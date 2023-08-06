# Copyright 2020 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

from pytket.circuit import Circuit
import networkx as nx
import graphviz as gv
from collections import defaultdict
from itertools import combinations
from tempfile import NamedTemporaryFile


class Graph:
    def __init__(self, c):
        """
        A class for visualising a circuit as a directed acyclic graph (DAG).

        :param      c:    Circuit
        :type       c:    pytket.Circuit
        """
        (
            q_inputs,
            c_inputs,
            q_outputs,
            c_outputs,
            input_names,
            output_names,
            node_data,
            edge_data,
        ) = c._dag_data
        self.q_inputs = q_inputs
        self.c_inputs = c_inputs
        self.q_outputs = q_outputs
        self.c_outputs = c_outputs
        self.input_names = input_names
        self.output_names = output_names
        self.node_data = node_data
        self.Gnx = None
        self.G = None
        self.Gqc = None
        self.edge_data = defaultdict(list)
        self.port_counts = defaultdict(int)
        for src_node, tgt_node, src_port, tgt_port, edge_type in edge_data:
            self.edge_data[(src_node, tgt_node)].append((src_port, tgt_port, edge_type))
            self.port_counts[(src_node, src_port)] += 1

    def as_nx(self):
        """
        Return a logical representation of the circuit as a DAG.

        :returns:   Representation of the DAG
        :rtype:     networkx.MultiDiGraph
        """
        if self.Gnx is not None:
            return self.Gnx
        Gnx = nx.MultiDiGraph()
        for node, desc in self.node_data.items():
            Gnx.add_node(node, desc=desc)
        for nodepair, portpairlist in self.edge_data.items():
            src_node, tgt_node = nodepair
            for src_port, tgt_port, edge_type in portpairlist:
                Gnx.add_edge(
                    src_node,
                    tgt_node,
                    src_port=src_port,
                    tgt_port=tgt_port,
                    edge_type=edge_type,
                )

        # Add node IDs to edges
        for edge in nx.topological_sort(nx.line_graph(Gnx)):
            src_node, tgt_node, i = edge
            # List parent edges with matching port number
            src_port = Gnx.edges[edge]["src_port"]
            prev_edges = [
                e
                for e in Gnx.in_edges(src_node, keys=True)
                if Gnx.edges[e]["tgt_port"] == src_port
            ]
            if not prev_edges:
                # The source must be an input node
                unit_id = src_node
                nx.set_edge_attributes(Gnx, {edge: {"unit_id": unit_id}})
            else:
                # The parent must be unique
                assert len(prev_edges) == 1
                prev_edge = prev_edges[0]
                unit_id = Gnx.edges[prev_edge]["unit_id"]
                nx.set_edge_attributes(Gnx, {edge: {"unit_id": unit_id}})
        # Sanity check: output names should match up
        for out_node, out_name in self.output_names.items():
            for e in Gnx.in_edges(out_node, keys=True):
                assert self.input_names[Gnx.edges[e]["unit_id"]] == out_name

        # Remove unnecessary port attributes to avoid clutter:
        for node in Gnx.nodes:
            if Gnx.out_degree(node) == 1:
                for edge in Gnx.out_edges(node, keys=True):
                    nx.set_edge_attributes(Gnx, {edge: {"src_port": None}})
            if Gnx.in_degree(node) == 1:
                for edge in Gnx.in_edges(node, keys=True):
                    nx.set_edge_attributes(Gnx, {edge: {"tgt_port": None}})

        self.Gnx = Gnx
        return Gnx

    def get_DAG(self):
        """
        Return a visual representation of the DAG as a graphviz object.

        :returns:   Representation of the DAG
        :rtype:     graphviz.DiGraph
        """
        if self.G is not None:
            return self.G
        G = gv.Digraph("Circuit", strict=True,)
        G.attr(rankdir="LR")
        q_color = "blue"
        c_color = "slategray"
        cr_color = "gray"
        gate_color = "lightblue"
        boundary_cluster_attr = {"style": "rounded, filled", "color": "lightgrey"}
        boundary_node_attr = {"fontname": "Courier", "fontsize": "8"}
        with G.subgraph(name="cluster_q_inputs") as c:
            c.attr(rank="source", **boundary_cluster_attr)
            c.node_attr.update(shape="point", color=q_color)
            for node in self.q_inputs:
                c.node(str(node), xlabel=self.input_names[node], **boundary_node_attr)
        with G.subgraph(name="cluster_c_inputs") as c:
            c.attr(rank="source", **boundary_cluster_attr)
            c.node_attr.update(shape="point", color=c_color)
            for node in self.c_inputs:
                c.node(str(node), xlabel=self.input_names[node], **boundary_node_attr)
        with G.subgraph(name="cluster_q_outputs") as c:
            c.attr(rank="sink", **boundary_cluster_attr)
            c.node_attr.update(shape="point", color=q_color)
            for node in self.q_outputs:
                c.node(str(node), xlabel=self.output_names[node], **boundary_node_attr)
        with G.subgraph(name="cluster_c_outputs") as c:
            c.attr(rank="sink", **boundary_cluster_attr)
            c.node_attr.update(shape="point", color=c_color)
            for node in self.c_outputs:
                c.node(str(node), xlabel=self.output_names[node], **boundary_node_attr)
        boundary_nodes = self.q_inputs | self.c_inputs | self.q_outputs | self.c_outputs
        Gnx = self.as_nx()
        for node, ndata in Gnx.nodes.items():
            if node not in boundary_nodes:
                G.node(
                    str(node),
                    shape="box",
                    style="rounded, filled",
                    color=gate_color,
                    fontname="Times-Roman",
                    fontsize="10",
                    label=ndata["desc"],
                )
        edge_colors = {
            0: q_color,  # Quantum
            1: cr_color,  # ClassicalRead
            2: c_color,  # ClassicalWrite
        }
        port_node_attr = {
            "shape": "point",
            "width": "0.0",
            "style": "invis",
        }
        edge_attr = {
            "weight": "2",
            "fontname": "Helvetica",
            "fontsize": "8",
            "labeldistance": "0.3",
            "labelangle": "180",
            "headclip": "true",
            "tailclip": "true",
        }
        for edge, edata in Gnx.edges.items():
            src_node, tgt_node, _ = edge
            src_port = edata["src_port"]
            tgt_port = edata["tgt_port"]
            edge_type = edata["edge_type"]
            src_nodename = str(src_node)
            tgt_nodename = str(tgt_node)
            main_srcname = src_nodename
            main_tgtname = tgt_nodename
            main_headlabel = ""
            main_taillabel = ""
            port_edge_color = q_color if edge_type == 0 else c_color
            if src_port is not None:
                if self.port_counts[(src_node, src_port)] == 1:
                    main_taillabel = str(src_port)
                else:
                    src_port_nodename = str((src_node, src_port, "out"))
                    G.node(src_port_nodename, label="", **port_node_attr)
                    G.edge(
                        src_nodename,
                        src_port_nodename,
                        taillabel=str(src_port),
                        color=port_edge_color,
                        arrowhead="none",
                        **edge_attr
                    )
                    main_srcname = src_port_nodename
            if tgt_port is not None:
                main_headlabel = str(tgt_port)
            G.edge(
                main_srcname,
                main_tgtname,
                arrowhead="vee",
                arrowsize="0.2",
                headlabel=main_headlabel,
                taillabel=main_taillabel,
                color=edge_colors[edge_type],
                **edge_attr
            )
        self.G = G
        return G

    def save_DAG(self, name, format="pdf"):
        """
        Save an image of the DAG to a file.

        The actual filename will be "<name>.<format>". A wide range of formats is
        supported. See https://graphviz.org/doc/info/output.html.

        :param      name:   Prefix of file name
        :type       name:   str
        :param      format: File format, e.g. "pdf", "png", ...
        :type       format: str
        """
        G = self.get_DAG()
        G.render(name, cleanup=True, format=format, quiet=True)

    def view_DAG(self):
        """
        View the DAG.
        """
        G = self.get_DAG()
        file = NamedTemporaryFile()
        G.view(file.name, quiet=True)

    def get_qubit_graph(self):
        """
        Return a visual representation of the qubit connectivity graph as a graphviz object.

        :returns:   Representation of the qubit connectivity graph of the circuit
        :rtype:     graphviz.Graph
        """
        if self.Gqc is not None:
            return self.Gqc
        Gnx = self.as_nx()
        Gqcnx = nx.Graph()
        for node in Gnx.nodes():
            qubits = []
            for e in Gnx.in_edges(node, keys=True):
                unit_id = Gnx.edges[e]["unit_id"]
                if unit_id in self.q_inputs:
                    qubits.append(unit_id)

            Gqcnx.add_edges_from(combinations(qubits, 2))
        G = gv.Graph(
            "Qubit connectivity",
            node_attr={
                "shape": "circle",
                "color": "blue",
                "fontname": "Courier",
                "fontsize": "10",
            },
            engine="neato",
        )
        G.edges(
            (self.input_names[src], self.input_names[tgt]) for src, tgt in Gqcnx.edges()
        )
        self.Gqc = G
        return G

    def view_qubit_graph(self):
        """
        View the qubit connectivity graph.
        """
        G = self.get_qubit_graph()
        file = NamedTemporaryFile()
        G.view(file.name, quiet=True)

    def save_qubit_graph(self, name, format="pdf"):
        """
        Save an image of the qubit connectivity graph to a file.

        The actual filename will be "<name>.<format>". A wide range of formats is
        supported. See https://graphviz.org/doc/info/output.html.

        :param      name:   Prefix of file name
        :type       name:   str
        :param      format: File format, e.g. "pdf", "png", ...
        :type       format: str
        """
        G = self.get_qubit_graph()
        G.render(name, cleanup=True, format=format, quiet=True)
