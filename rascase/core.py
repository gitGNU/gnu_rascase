# -*- coding: utf-8 -*-
"""
Este modulo contiene las clases que pertenecen al modelo del patron MVC++

"""
##
## core.py
## Login : <freyes@yoda>
## Started on  Fri Feb  1 12:46:21 2008 Felipe Reyes
## $Id$
## 
## Copyright (C) 2008 Felipe Reyes
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##

import gconf
import xml.dom.minidom
import xml.dom.ext
import logging
import os

from datetime import datetime
from time import time
from pkg_resources import resource_filename

log = logging.getLogger("core")

XML_URI = "http://freyes.linuxdiinf.org/rascase"

class ModelBase:
    """clase base para la implementación de las clases modelo"""
    def __init__(self, path):
        self._name = None
        self._path = path

    def save(self, path=None):
        raise NotImplemented

    def get_path(self):
        return self._path

    def print_model(self):
        return False

    def export_to_png(self):
        return False

    def check(self):
        raise NotImplemented

    #metodos para enriquecer la clase
    def __eq__(self, y):
        """Retorna True si los dos objetos usan el mismo path para el archivo, en caso contrario retorna False"""
        if not(y.__class__ is ModelBase):
            return False
        elif (self._path == y.get_path()):
            return True
        else:
            return False

    def __ne__(self, y):
        """Retorna False si los objetos utilizan rutas distintas para almacenar el proyecto, en caso contrario retorna True"""
        if not(y.__class__ is ModelBase):
            return False
        elif (self._path != y.get_path()):
            return True
        else:
            return False

class LogicalBase:
    def __init__(self):
        self._name = None
        self._codename = None
        self._description = None

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_codename(self):
        return self._codename

    def set_codename(self, value):
        self._codename = value

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

    def to_xml(self, doc, uri):
        raise NotImplemented

    def check(self):
        raise NotImplemented

class RectBase:
    def __init__(self):
        self._linecolor = None
        self._linewidth = None
        self._fillcolor = None
        self._width = None
        self._height = None
        self._pos_x = None
        self._pos_y = None
        self._dragbox = None

    def set_linecolor(self, value):
        self._linecolor = value

    def get_linecolor(self):
        return self._linecolor

    def set_linewidth(self, value):
        self._linewidth = value

    def get_linewidth(self):
        return self._linewidth

    def set_fillcolor(self, value):
        self._fillcolor = value

    def get_fillcolor(self):
        return self._fillcolor

    def set_width(self, value):
        self._width = value

    def get_width(self):
        return self._width

    def set_height(self, value):
        self._height = value

    def get_height(self):
        return self._height

    def set_x(self, value):
        self._pos_x = value

    def get_x(self):
        return self._pos_x

    def set_y(self, value):
        self._pos_y = value

    def get_y(self):
        return self._pos_y

class ConfigurationManager:
    def __init__(self):
        self._client = gconf.client_get_default()
        self._client.add_dir('/apps/rascase', gconf.CLIENT_PRELOAD_NONE)

    def get_entity_color(self):
        res = self._client.get_string('/apps/rascase/entity_color')
        print 'entity_color: ', res
        return res

    def set_entity_color(self, value):
        self._client.set_string('/apps/rascase/entity_color', value)

    def add_recently_opened(self,path):
        pass

    def set_label_color(self, value):
        self._client.set_string('/apps/rascase/label_color', value)

    def get_label_color(self):
        return self._client.get_label_color('/apps/rascase/label_color')

    def set_relationship_color(self, value):
        self._client.set_string('/apps/rascase/relationship_color', value)

    def get_relationship_color(self):
        return self._client.get_string('/apps/rascase/relationship_color')

    def set_table_color(self, value):
        self._client.set_string('/apps/rascase/table_color', value)

    def get_table_color(self):
        return self._client.get_string('/apps/rascase/table_color')

    def set_reference_color(self, value):
        self._client.set_string('/apps/rascase/reference_color', value)

    def get_reference_color(self):
        return self._client.get_string('/apps/rascase/reference_color')

    def set_inheritance_color(self, value):
        self._client.set_string('/apps/rascase/inheritance_color', value)

    def get_inheritance_color(self):
        return self._client.get_string('/apps/rascase/inheritance_color')

    def set_last_project_opened(self, path):
        self._client.set_string('/apps/rascase/last_project', value)

    def get_last_project_opened(self):
        return self._client.get_string('/apps/rascase/last_project')

class Project:
    def __init__(self, filepath=None):
        """Construye un proyecto y los modelos asociados a este

        Si no es pasada la ruta de un proyecto como parámetro (opicon por defecto) se construye un proyecto vacio, es decir, con las opciones por defecto y sin modelos asociados"""
        ## self._name = None
        self._path = filepath
        self._models_list = list()

        doc = xml.dom.minidom.parse(self._path)
        projectnode = doc.childNodes[0]

        for node in projectnode.childNodes:
            if node.nodeType == node.TEXT_NODE:
                continue

            modelname = node.getAttributeNS(XML_URI, 'modelpath')

            log.info("found the model %s inside project %s", modelname, self._path)

            # we get the extension of the filename
            extension = os.path.basename(modelname).split('.', 2)[1]
            log.debug("extension of %s is %s", modelname, extension)

            #rxl == rascase xml logical
            #rxf == rascase xml fisico (physical in spanish)
            if (extension == "rxl"):
                self._models_list.append(logical.LogicalModel(path=modelname))
            elif (extension == "rxf"):
                self._models_list.append(PhysicalModel(path=modelname))
            else:
                print "problemas con la extension: ", extension
                print os.path.basename(modelname), modelname

    ## #averiguar para que mierda puse la propiedad 'name'
    ## def set_name(self, name):
    ##     pass

    def get_name(self):
        "Retorna el nombre del archivo, puede ser usado para ponerlo en el titulo de la ventana"
        return os.path.basename(self._path)

    def add_model(self, model):
        if not(type(model) is ModelBase):
            log.error("The argument passed to %s.add_model is not a ModelBase instance (%s)", self, model)
            raise RuntimeError
        elif (model in self._models_list): #this only checks the references, _not_ the path
            log.debug("Trying to add to the project an already existing model")
            return False

        self._models_list.append(model)
        return True

    def get_models(self):
        """Retorna la lista de modelos asociados al proyecto"""
        return self._models_list

    def del_model(self, model, del_from_disk=False):
        """Elimina el objeto modelo pasado como y opcionalmente borra el archivo asociado al modelo (por defecto no lo hace)

        Si la operación se lleva a cabo con éxito returna True, en caso contrario retorna False y escribe en el log el problema"""
        if not(model in self._models_list):
            log.debug("Trying to delete a model that does not exist in the project")
            return False
        else:
            if (self._models_list.count(model) != 1):
                log.error("The model %s is %s in the project", model, self._models_list.count(model))
                return False
            if (del_from_disk):
                filepath = model.get_path()
                self._models_list.remove(model)
                os.remove(filepath)
            else:
                self._models_list.remove(model)
            return True

    def save(self, path=None):
        """Almacena el proyecto en el archivo pasado como parámetro o el utilizado la última vez que se guardó el proyecto"""
        doc = xml.dom.minidom.Document()

        # crete the project node and add it to the document
        prj = doc.createElementNS(URI_XML, "ras:project")
        doc.appendChild(prj)

        for i in range(len(self._models_list)):
            model = doc.createElementNS(XML_URI, "ras:model")
            model.setAttributeNS(XML_URI, "ras:modelpath", self._models_list[i].get_path())
            prj.appendChild(model)

        if path!=None:
            self._path = path

        file_out = open(self._path, "w")
        xml.dom.ext.PrettyPrint(doc, file_out)

class Print:
    """Esta clase se encarga de imprimir"""
    pass
class LogicalModel(base.ModelBase):
    def __init__(self, path=None):
        log.debug("LogicalModel.__init__(path=%s)", path)
        base.ModelBase.__init__(self, path)
        self._entities_list = list()
        self._relationships_list = list()
        self._inheritance_list = list()

        # if the path given is None, then we use an empty model provided by the software
        if (self._path == None):
            now = datetime.fromtimestamp(time())
            newmodelname = str(now.year) + str(now.month) + str(now.day) + \
                           str(now.hour) + str(now.minute) + str(now.second) + '.rxl'
            srcname = resource_filename('rascase.resources', 'sample_logical_model.rxl')
            dstname = os.path.join('/tmp/', newmodelname)
            try:
                copy(srcname, dstname)
            except (IOError, os.error), why:
                log.debug("Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why)))

            self._path = dstname

        #now we must construct the logical model
        doc = xml.dom.minidom.parse(self._path)
        modelo = doc.childNodes[0]

        for i in modelo.childNodes:
            if i.nodeType == i.TEXT_NODE:
                print "datos: '", i.data, "'"


    def generate_physical_model(self, path=None):
        return False

    def add_entity(self, entity):
        self._entities_list.append(entity)

    def get_entity(self, codename):
        return None

    def del_entity(self, codename):
        return False

    def get_all_entites(self):
        return self._entities_list

    def save(self, path=None):
        """Almacena el modelo en el archivo pasado como parámetro o el utilizado la última vez que se guardó el modelo"""
        log.debug("Saving the Logical model %s", self._path)

        doc = xml.dom.minidom.Document()

        # crete the logicalmodel node and add it to the document
        logicalmodel = doc.createElementNS(XML_URI, "ras:logicalmodel")
        doc.appendChild(logicalmodel)

        # generate the xml for the entities
        for i in range(len(self._entities_list)):
            log.debug("saving entity: %s", self._entities_list[i].get_codename())
            entity_node = self._entities_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(entity_node)

        #generate the xml for the relationships
        for i in range(len(self._relationships_list)):
            log.debug("saving relationship: %s", self._relationships_list[i].get_codename())
            relationship_node = self._relationships_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(relationship_node)

        # generate the xml for the inheritances
        for i in range(len(self._inheritance_list)):
            log.debug("saving inheritance: %s", self._inheritance_list[i].get_codename())
            inheritance_node = self._inheritance_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(inheritance_node)

        # if there is some path given by parameter will be used
        if path!=None:
            self._path = path

        # write the xml into a file
        xml.dom.ext.PrettyPrint(doc, open(self._path, "w"))



class Entity(LogicalBase, RectBase):
    def __init__(self, x=0, y=0, xmlnode=None):
        LogicalBase.__init__(self)
        RectBase.__init__(self)
        self._attributes_list = list()

        if (xmlnode != None):
            self.set_name(xmlnode.getAttributeNS(XML_URI, "ras:name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "ras:codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "ras:description"))

            #get the position of the entity
            self.set_x(xmlnode.getAttributeNS(XML_URI, "ras:x"))
            self.set_y(xmlnode.getAttributeNS(XML_URI, "ras:y"))

            #get the dimentions of the entity
            self.set_height(xmlnode.getAttributeNS(XML_URI, "ras:height"))
            self.set_width(xmlnode.getAttributeNS(XML_URI, "ras:width"))

            #get the visual properties of the entity
            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "ras:linecolor"))
            self.set_linewidth(xmlnode.getAttributeNS(XML_URI, "ras:linewidth"))
            self.set_fillcolor(xmlnode.getAttributeNS(XML_URI, "ras:fillcolor"))

            


    def add_attribute(self, attribute):
        return False

    def del_attribute(self, attribute):
        return False

    def to_xml(self, doc, uri):
        """Transforma la información que almacena el objeto en un nodo xml y lo retorna"""
        entity = doc.createElementNS(uri, "ras:entity")

        entity.setAttributeNS(uri, "ras:name", self.get_name())
        entity.setAttributeNS(uri, "ras:codename", self.get_codename())
        entity.setAttributeNS(uri, "ras:description", self.get_description())

        entity.setAttributeNS(uri, "ras:x", self.get_x())
        entity.setAttributeNS(uri, "ras:y", self.get_y())

        entity.setAttributeNS(uri, "ras:height", self.get_height())
        entity.setAttributeNS(uri, "ras:width", self.get_width())

        entity.setAttributeNS(uri, "ras:linecolor", self.get_linecolor())
        entity.setAttributeNS(uri, "ras:linewidth", self.get_linewidth())
        entity.setAttributeNS(uri, "ras:fillcolor", self.get_fillcolor())

        for i in range(len(self._attributes_list)):
            log.debug("to xml %s.%s", self.get_codename(),
                      self._attributes_list[i].get_codename())
            attrnode = self._attributes_list[i].to_xml(doc, uri)
            entity.appendChild(attrnode)

        return entity

class Attribute(LogicalBase):
    def __init__(self):
        self._primary_key = False
        self._data_type = None
        self._default_value = None
        self._mandatory = False

    def set_primary_key(self, value):
        pass

    def is_primary_key(self):
        return False

    def set_default_value(self, value):
        pass

    def get_default_value(self):
        pass

    def set_data_type(self, value):
        pass

    def get_data_type(self):
        pass

    def set_mandatory(self, value):
        pass

    def is_mandatory(self):
        pass


class Relationship(LogicalBase):

    CARDINALITY_1_1 = 0
    CARDINALITY_1_N = 1
    CARDINALITY_N_1 = 2
    CARDINALITY_N_N = 3
    
    def __init__(self, entity1, entity2):
        self._cardinality = None
        self._entity1 = entity1
        self._entity2 = entity2

    def set_cardinality(self, value):
        pass

    def get_cardinality(self):
        pass

    def set_entity1(self, entity):
        pass

    def get_entity1(self):
        pass

    def set_entity2(self, entity):
        pass

    def get_entity2(self):
        pass

class Inheritance(LogicalBase):
    def __init__(self, father, son):
        self._father = father
        self._son = son

class LogicalDataType:
    CHARACTER = 0
    VARCHAR = 1
    BIT = 2
    VARBIT = 3
    NUMERIC = 4
    DECIMAL = 5
    INTEGER = 6
    SMALLINT = 7
    FLOAT = 8
    REAL = 9
    DOUBLE = 10
    DATE = 11
    TIME = 12
    TIMESTAMP = 13
    INTERVAL = 14

    def to_string(cls, type):
        pass
    to_string = classmethod(to_string) #transforma el metodo to_string en estatico

    def get_description(cls, type):
        pass

    get_description = classmethod(get_description)

class Label(RectBase):
    def __init__(self, text):
        self._text = ""

    def set_text(self, text):
        pass

    def get_text(self):
        pass


class Rectangle(RectBase):
    def __init__(self, x, y):
        self.set_x = x
        self.set_y = y

class PhysicalBase:
    def __init__(self):
        self._name = None
        self._codename = None
        self._description = None

    def set_name(self, name):
        pass

    def get_name(self):
        pass

    def set_codename(self, codename):
        pass

    def get_codename(self):
        pass

    def set_description(self, description):
        pass

    def check(self):
        pass

    


class PhysicalModel(ModelBase):
    def __init__(self, logicalmodel=None, path=None):
        log.debug("PhysicalModel.__init__(logicalmodel=%s, path=%s)", logicalmodel, path)
        self._script_plugin = None
        self._dict_plugin = None
        self._tables_list = None
        self._references = None

    def generate_script(self, path=None):
        return False

    def generate_dictionary(self, path=None):
        return False

    def set_script_plugin(self, plugin):
        pass

    def get_script_plugin(self):
        return self._script_plugin

    def set_dict_plugin(self, plugin):
        pass

    def get_dict_plugin(self):
        return self._dict_plugin

class Table:
    def __init__(self):
        self._columns_list = None

    def add_column(self, column):
        pass

    def del_column(self, column):
        pass

class Column(PhysicalBase):
    def __init__(self):
        self._primary_key = False
        self._data_type = None
        self._default_value = None
        self._mandatory = False

    def set_primary_key(self, value):
        pass

    def is_primary_key(self):
        return False

    def set_default_value(self, value):
        pass

    def get_default_value(self):
        pass

    def set_data_type(self, value):
        pass

    def get_data_type(self):
        pass

    def set_mandatory(self, value):
        pass

    def is_mandatory(self):
        pass

class Reference:
    def __init__(self, table1, table2):
        self._table1 = table1
        self._table2 = table2

    def set_table1(self, table):
        pass

    def get_table1(self, table):
        pass

    def set_table2(self, table):
        pass

class PhysicalDataType:
    CHARACTER = 0
    VARCHAR = 1
    BIT = 2
    VARBIT = 3
    NUMERIC = 4
    DECIMAL = 5
    INTEGER = 6
    SMALLINT = 7
    FLOAT = 8
    REAL = 9
    DOUBLE = 10
    DATE = 11
    TIME = 12
    TIMESTAMP = 13
    INTERVAL = 14

    def to_string(cls, type):
        pass
    to_string = classmethod(to_string) #transforma el metodo to_string en estatico

    def get_description(cls, type):
        pass

    get_description = classmethod(get_description)
