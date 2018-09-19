import re, markdown

import os
from markdown.util import etree
import markdown_phantom_plot
import xml.etree.ElementTree as ET


class PhantomPlotExtension(markdown.Extension):
    def __init__(self, configs=None):
        pass

    def extendMarkdown(self, md, md_globals):
        self.md = md
        md.treeprocessors.add('phantom-plot', PhantomPlotTreeProcessor(), "_end")

    def reset(self):
        pass

def process_plot_query(node, x):
    inf = x
    outf = os.path.splitext(inf)[0] + ".svg"
    try:
        markdown_phantom_plot.plot_file(inf, outf)
        with open(outf, "r") as f:
            node.append(ET.fromstring("<img style='width:100%' src='"+outf+"'></img>"))
            node.tag = "div"
    except Exception as e:
        node.append(ET.fromstring("<p style='color:red;font-weight:bold;'>" + str(e) + "</p>"))


class PhantomPlotTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def run(self, node):
        if node.getchildren():
            for child in node.getchildren():
                self.run(child)
        if node.tag != "p":
             return node

        RE = r'\s*PLOT\s+([^\s]+)\s*'
        m = re.match(RE, node.text)
        if m:
            process_plot_query(node, m.group(1))
        return node

def makeExtension(configs=None):
    return PhantomPlotExtension(configs=configs)
