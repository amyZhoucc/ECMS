#-*- coding:utf-8 -*-
import sys
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def loadXML(xml):
    xml = xml
    try:
        tree = ET.parse(xml)
    except:
        print("load %s error"%xml)
        raise
    return tree

def getNode(root,nodeName):
    return  root.iter(nodeName)

def getTag(root,tagName):
    return root.iter(tagName)

#获取xml中的子节点，插入到tree中
def insertElementFromXML(xml,tree,parentTageName,childTagName):
    tree1 = loadXML(xml)
    subelement = tree1.getiterator(childTagName)
    parentelement = tree.getiterator(parentTageName)
    for sub in subelement:
        parentelement[0].append(sub)
    return tree

def getElementByAttribute(tree,parentTagName,childTagName,attributeName):
    parent = tree.getiterator(parentTagName)
    datas = dict()
    for child in parent[0].iter(childTagName):
        datas[child.attrib[attributeName]] = child.text
    return datas

def getElementTextByTag(tree,parentTagName,childTagName):
    parent = tree.getiterator(parentTagName)
    datas = list()
    for child in parent[0].iter(childTagName):
        datas.append(child.text)
    return datas

def deleteElementByAttribute(tree,parentTagName,childTagName,attributeName,attributeValue):
    parent = tree.getiterator(parentTagName)
    for child in parent[0].iter(childTagName):
        if child.attrib[attributeName] == attributeValue:
            print("delete %s"%child.attrib[attributeName])
            parent[0].remove(child)
            break
    return tree

#有错误
#根据属性及其属性值，将tree中的对应子节点替换为xml中的子节点
def replaceElementFromXMLByAttribute(xml,tree,parentTagName,childTagName,attributeName,attributeValue):
    tree1 = loadXML(xml)
    newelement = tree1.getiterator(childTagName)
    tree = deleteElementByAttribute(tree,parentTagName,childTagName,attributeName,attributeValue)
    #
    tree = insertElementFromXML(xml,tree,parentTagName,childTagName)
    #
    return tree

def modifyElementText(tree,tagName,text):
    element = tree.getiterator(tagName)
    element[0].text = text
    return tree

def saveXML(tree,xmlfile):
    tree.write(xmlfile,encoding='UTF-8')

def main():
    tree = loadXML("conf.xml")
    #tree = insertElementFromXML("AR-arrm.xml",tree,"components","component")
    #tree = replaceElementFromXMLByAttribute("arrm.xml",tree,"components","component","id","arrm")
    #tree = modifyElementText(tree,"expirDate","2020-01-01")
    # saveXML(tree,"output_new.xml")
    selections = getElementByAttribute(tree,"SearchSelection","selection","value")
    deps = getElementTextByTag(tree,"Departments","department")
    print(selections)
    print(deps)

if __name__ == "__main__":
    main()