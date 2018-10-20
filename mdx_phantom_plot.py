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
        self.ppt = PhantomPlotTreeProcessor(md);
        md.treeprocessors.add('phantom-plot', self.ppt, "_end")

    def kill(self):
        markdown_phantom_plot.phantom.kill()

    def reset(self):
        self.ppt.reset()


def process_plot_query(node, x, ext, plotID):
    try:
        os.mkdir("plots/")
    except:
        pass
    inf = "plots/%i.pp" % plotID
    with open(inf, "w") as f:
        f.write(x)

    outf = os.path.splitext(inf)[0] + "." + ext
    node.text = ""
    for child in list(node):
        node.remove(child)
    try:
        markdown_phantom_plot.plot_file(inf, outf)
        with open(outf, "r") as f:
            node.append(ET.fromstring("<img style='width:100%' src='"+outf+"'></img>"))
            node.tag = "div"
    except Exception as e:
        node.append(ET.fromstring("<p style='color:red;font-weight:bold;'>" + str(e) + "</p>"))


class PhantomPlotTreeProcessor(markdown.treeprocessors.Treeprocessor):
    def __init__(self, md):
        self.md = md
        self.plotID = 0

    def process(self, node, ext):
        if node.getchildren():
            for child in node.getchildren():
                self.process(child, ext)
        if node.tag != "p":
             return node

        try:
            if node.text == "PLOT":
                t = ""
                for child in node.getchildren():
                    t += child.tail
                process_plot_query(node, t, ext, self.plotID)
                self.plotID += 1
        except Exception as e:
            raise e
        return node

    def reset(self):
        self.plotID = 0

    def run(self, node):
        ext = "svg"
        for e in self.md.registeredExtensions:
            if e.__class__.__name__ == "LaTeXExtension":
                ext = "pdf"
        return self.process(node, ext)



def makeExtension(configs=None):
    return PhantomPlotExtension(configs=configs)
