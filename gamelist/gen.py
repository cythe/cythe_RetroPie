#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
from xml.dom.minidom import getDOMImplementation
from xml.dom import minidom
import xml

def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    writer.write(indent+"<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    sorted(a_names)

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s"%(newl))
        for node in self.childNodes:
            if node.nodeType is not minidom.Node.TEXT_NODE:
                node.writexml(writer,indent+addindent,addindent,newl)
        writer.write("%s</%s>%s" % (indent,self.tagName,newl))
    else:
        writer.write("/>%s"%(newl))

minidom.Element.writexml=fixed_writexml

def regen_xml(iterms):
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "shelf", None)
    top_element = newdoc.documentElement
    for i in iterms:
        top_element.appendChild(i)
    f=open("test.xml", "w")
    xml=newdoc.writexml(f, addindent='\t', newl='\n')

# 使用minidom解析器打开 XML 文档
doc = xml.dom.minidom.parse("movies.xml")
print(doc)
top = doc.documentElement
if top.hasAttribute("shelf"):
    print("Root element : {}".format(top.getAttribute("shelf")))

# 在集合中获取所有电影
movies = top.getElementsByTagName("movie")
print(movies)
movies.sort(key=lambda x:x.getAttribute("title"))
# 打印每部电影的详细信息
for movie in movies:
    print("*****Movie*****")
    print(movie)
    if movie.hasAttribute("title"):
        print("Title: {}".format(movie.getAttribute("title")))

    type = movie.getElementsByTagName('type')[0]
    print("Type: {}".format(type.childNodes[0].data))
    format = movie.getElementsByTagName('format')[0]
    print("Format: {}".format(format.childNodes[0].data))
    rating = movie.getElementsByTagName('rating')[0]
    print("Rating: {}".format(rating.childNodes[0].data))
    description = movie.getElementsByTagName('description')[0]
    print("Description: {}".format(description.childNodes[0].data))

mynode=doc.createElement("movie")
mynode.setAttribute("title", "Mymovie")
element = doc.createElement("new")
element.appendChild(doc.createTextNode("Anydata"))
mynode.appendChild(element)
top.appendChild(mynode)

f=open("movies1.xml", "w")
xml=doc.writexml(f, addindent='\t', newl='\n')
regen_xml(movies)
