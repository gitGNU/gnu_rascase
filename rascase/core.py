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
from shutil import copy
from pkg_resources import resource_filename

log = logging.getLogger("core")

XML_URI = "http://freyes.linuxdiinf.org/rascase"

class ModelBase:
    """clase base para la implementación de las clases modelo"""
    def __init__(self, path):
        self._name = None #para que sirve esto?
        self._path = path

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._path = path

    def print_model(self):
        raise NotImplemented

    def export_to_png(self):
        raise NotImplemented

    def save(self, path=None):
        raise NotImplemented

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
        self._name = str()
        self._codename = str()
        self._description = str()

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
        #TODO: define the default colors
        self._linecolor = None
        self._linewidth = None
        self._fillcolor = None
        self._width = None
        self._height = None
        self._pos_x = None
        self._pos_y = None
        self._dragbox = None #creo que esto no es necesario, pk ni siquiera para que lo puse :P

    def set_linecolor(self, value):
        "Define el color de la linea del rectangulo"
        self._linecolor = value

    def get_linecolor(self):
        "Retorna el color de la linea del rectangulo"
        return self._linecolor

    def set_linewidth(self, value):
        "Define el ancho de la linea del borde del rectángulo en pixeles"
        self._linewidth = value

    def get_linewidth(self):
        "Retorna el ancho de la linea del borde del rectángulo en pixeles"
        return self._linewidth

    def set_fillcolor(self, value):
        "Define el color con que se rellena el rectángulo"
        self._fillcolor = value

    def get_fillcolor(self):
        "Retorna el color con que se rellena el rectángulo"
        return self._fillcolor

    def set_width(self, value):
        "Define el ancho del rectángulo en pixeles"
        self._width = value

    def get_width(self):
        "Retorna el ancho del rectángulo en pixeles"
        return self._width

    def set_height(self, value):
        "Define el alto del rectángulo en pixeles"
        self._height = value

    def get_height(self):
        "Retorna el alto del rectángulo en pixeles"
        return self._height

    def set_x(self, value):
        "Define la posición (en pixeles) en el eje X de la esquina superior izquierda"
        self._pos_x = value

    def get_x(self):
        "Retorna la posición (en pixeles) en el eje X de la esquina superior izquierda"
        return self._pos_x

    def set_y(self, value):
        "Define la posición (en pixeles) en el eje Y de la esquina superior izquierda"
        self._pos_y = value

    def get_y(self):
        "Retorna la posición (en pixeles) en el eje X de la esquina superior izquierda"
        return self._pos_y

class ConfigurationManager:
    def __init__(self):
        self._base_dir = '/apps/rascase'
        self._client = gconf.client_get_default()
        self._client.add_dir(self._base_dir, gconf.CLIENT_PRELOAD_NONE)

    def get_entity_color(self):
        res = self._client.get_string(self._base_dir + '/entity_color')
        log.debug('entity_color: %s', res)
        return res

    def set_entity_color(self, value):
        self._client.set_string(self._base_dir + '/entity_color', value)

    def add_recently_opened(self,path):
        pass

    def set_label_color(self, value):
        self._client.set_string(self._base_dir + '/label_color', value)

    def get_label_color(self):
        return self._client.get_label_color(self._base_dir + '/label_color')

    def set_relationship_color(self, value):
        self._client.set_string(self._base_dir + '/relationship_color', value)

    def get_relationship_color(self):
        return self._client.get_string(self._base_dir + '/relationship_color')

    def set_table_color(self, value):
        self._client.set_string(self._base_dir + '/table_color', value)

    def get_table_color(self):
        return self._client.get_string(self._base_dir + '/table_color')

    def set_reference_color(self, value):
        self._client.set_string(self._base_dir + '/reference_color', value)

    def get_reference_color(self):
        return self._client.get_string(self._base_dir + '/reference_color')

    def set_inheritance_color(self, value):
        self._client.set_string(self._base_dir + '/inheritance_color', value)

    def get_inheritance_color(self):
        return self._client.get_string(self._base_dir + '/inheritance_color')

    def set_last_project_opened(self, value):
        self._client.set_string(self._base_dir + '/last_project', value)

    def get_last_project_opened(self):
        return self._client.get_string(self._base_dir + '/last_project')

class Project:
    def __init__(self, filepath=None):
        """Construye un proyecto y los modelos asociados a este

        Si no es pasada la ruta de un proyecto como parámetro (opcion por defecto)
        se construye un proyecto vacio, es decir, con las opciones por defecto
        y sin modelos asociados

        """
        ## self._name = None
        self._path = filepath
        self._models_list = list()

        if os.path.isfile(self._path):
            doc = xml.dom.minidom.parse(self._path)
            projectnode = doc.childNodes[0]

            for node in projectnode.getElementsByTagNameNS(XML_URI, "model"):
                modelname = node.getAttributeNS(XML_URI, 'modelpath')

                log.info("found the model %s inside project %s",
                         modelname, self._path)

                # we get the extension of the filename
                extension = os.path.basename(modelname).split('.', 2)[1]
                log.debug("extension of %s is %s", modelname, extension)

                #rxl == rascase xml logical
                #rxf == rascase xml fisico (physical in spanish)
                if (extension == "rxl"):
                    self._models_list.append(LogicalModel(path=modelname))
                elif (extension == "rxf"):
                    self._models_list.append(PhysicalModel(path=modelname))
                else:
                    log.debug("problems with the extension: %s of %s",
                              extension, modelname)
            else:
                log.debug("The project is empty")
        else:
            log.debug("The path: %s is not a file", self._path)

    ## #averiguar para que mierda puse la propiedad 'name'
    ## def set_name(self, name):
    ##     pass

    def get_name(self):
        """Retorna el nombre del archivo

        Puede ser usado para ponerlo en el titulo de la ventana

        """
        return os.path.basename(self._path)

    def add_model(self, model):
        "Agrega un modelo al proyecto"
        if not isinstance(model, ModelBase):
            log.error("The argument passed to %s.add_model is not a \
            ModelBase instance (%s)",
                      self, model)
            raise RuntimeError

        #this only checks the references, _not_ the path
        elif (model in self._models_list):
            log.debug("Trying to add to the project an already existing model")
            return False

        self._models_list.append(model)
        return True

    def get_models(self):
        "Retorna la lista de modelos asociados al proyecto"
        return self._models_list

    def del_model(self, model, del_from_disk=False):
        """Elimina el objeto modelo pasado como y opcionalmente borra el archivo
        asociado al modelo (por defecto no lo hace)

        Si la operación se lleva a cabo con éxito returna True, en caso contrario
        retorna False y escribe en el log el problema

        """
        if not(model in self._models_list):
            log.debug("Trying to delete a model that does not exist in the project")
            return False
        else:
            if (self._models_list.count(model) != 1):
                log.debug("The model %s is %s in the project",
                          model, self._models_list.count(model))
                return False
            if (del_from_disk):
                filepath = model.get_path()
                self._models_list.remove(model)
                os.remove(filepath)
            else:
                self._models_list.remove(model)
            return True

    def save(self, path=None):
        """Almacena el proyecto en el archivo pasado como parámetro o el
        utilizado la última vez que se guardó el proyecto

        """
        doc = xml.dom.minidom.Document()

        # crete the project node and add it to the document
        prj = doc.createElementNS(XML_URI, "project")
        doc.appendChild(prj)

        for i in range(len(self._models_list)):
            model = doc.createElementNS(XML_URI, "model")
            model.setAttributeNS(XML_URI, "modelpath",
                                 self._models_list[i].get_path())
            prj.appendChild(model)

        if path!=None:
            self._path = path

        xml.dom.ext.PrettyPrint(doc, open(self._path, "w"))
        log.debug("Project %s written", self._path)

#TODO: implementar esta clase y definir el comportamiento que debe tener
class Print:
    """Esta clase se encarga de imprimir"""
    def __init__(self):
        pass

class LogicalModel(ModelBase):
    "Esta clase representa un modelo lógico"
    def __init__(self, path=None):
        log.debug("LogicalModel.__init__(path=%s)", path)
        ModelBase.__init__(self, path)
        self._entities_list = list()
        self._relationships_list = list()
        self._inheritance_list = list()

        self._label_list = list()
        self._rectangle_list = list()

        # if the path given is None, then we use an empty model
        # provided by the software
        if (self._path == None):
            now = datetime.fromtimestamp(time())

            newmodelname = str(now.year) + str(now.month) + str(now.day) +\
                           str(now.hour) + str(now.minute) + str(now.second) +\
                           '.rxl'

            srcname = resource_filename('rascase.resources',
                                        'sample_logical_model.rxl')
            dstname = os.path.join('/tmp/', newmodelname)
            try:
                copy(srcname, dstname)
            except (IOError, os.error), why:
                log.debug("Can't copy %s to %s: %s", srcname, dstname, str(why))

            self._path = dstname

        #now we must construct the logical model
        doc = xml.dom.minidom.parse(self._path)
        modelo = doc.childNodes[0]

        # Entity
        for node in modelo.getElementsByTagNameNS(XML_URI, "entity"):
            log.debug("constructing an entity")
            entity = Entity(xmlnode=node)
            self._entities_list.append(entity)

        # Relationship
        for node in modelo.getElementsByTagNameNS(XML_URI, "relationship"):
            log.debug("construction a relationship")
            relationship = Relationship(xmlnode=node)
            self._relationships_list.append(relationship)

        # Inheritance
        for node in modelo.getElementsByTagNameNS(XML_URI, "inheritance"):
            log.debug("constructing a inheritance")
            inheritance = Inheritance(xmlnode=node)
            self._inheritance_list.append(inheritance)

        # Labels
        for node in modelo.getElementsByTagNameNS(XML_URI, "label"):
            log.debug("constructin a label")
            label = Label(xmlnode=node)
            self._label_list.append(label)

        # Rectangles
        for node in modelo.getElementsByTagNameNS(XML_URI, "rectangle"):
            log.debug("constructing a rectangle")
            rect = Rectangle(xmlnode=node)
            self._rectangle_list.append(rect)

    #TODO: implementar este metodo
    def generate_physical_model(self, path=None):
        pass

    def add_entity(self, entity):
        """Agrega la entidad dada al modelo

        Si la entidad es agregada con exito retorna True.

        """
        if not isinstance(entity, Entity):
            log.debug("Trying to add an object that is not an entity to a model")
            return False
        elif entity in  self._entities_list:
            log.debug("Trying to add an  entity that already exists \
            to the logical model")
            return False

        self._entities_list.append(entity)
        return True

    def get_entity(self, codename):
        """Retorna la entidad que tiene el codename dado.

        Si no se encuentra una entidad con el codename dado en el modelo se retorna None

        """
        for entity in self._entities_list:
            if (entity.get_codename() == codename):
                return entity
        else: #if the entity could not be founded return None
            return None

    def del_entity(self, codename):
        "Elimina la entidad que tiene el codename dado"
        for i in range(len(self._entities_list)):
            if (self._entities_list[i].get_codename() == codename):
                del self._entities_list[i]
                return True
        else:
            return False

    def get_all_entites(self):
        "Retorna una lista de entidades asociadas al modelo logico"
        return self._entities_list

    def save(self, path=None):
        """Almacena el modelo en el archivo pasado como parámetro o el utilizado
        la última vez que se guardó el modelo

        """
        log.debug("Saving the Logical model %s", self._path)

        doc = xml.dom.minidom.Document()

        # crete the logicalmodel node and add it to the document
        logicalmodel = doc.createElementNS(XML_URI, "ras:logicalmodel")
        doc.appendChild(logicalmodel)

        # generate the xml for the entities
        for entity in self._entities_list:
            log.debug("saving entity: %s", entity.get_codename())
            entity_node = entity.to_xml(doc, XML_URI)
            logicalmodel.appendChild(entity_node)

        #generate the xml for the relationships
        for relationship in self._relationships_list:
            log.debug("saving relationship: %s",
                      relationship.get_codename())
            relationship_node = relationship.to_xml(doc, XML_URI)
            logicalmodel.appendChild(relationship_node)

        # generate the xml for the inheritances
        for inheritance in self._inheritance_list:
            log.debug("saving inheritance: %s",
                      inheritance.get_codename())
            inheritance_node = inheritance.to_xml(doc, XML_URI)
            logicalmodel.appendChild(inheritance_node)

        # if there is some path given by parameter will be used
        if path!=None:
            self._path = path

        # write the xml into a file
        xml.dom.ext.PrettyPrint(doc, open(self._path, "w"))


class Entity(LogicalBase, RectBase):
    counter = int(0)

    def __init__(self, x=0, y=0, xmlnode=None):
        LogicalBase.__init__(self)
        RectBase.__init__(self)
        self.set_x(x)
        self.set_y(y)
        self._attributes_list = list()

        if (xmlnode != None):
            self.set_name(xmlnode.getAttributeNS(XML_URI, "name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "description"))

            #get the position of the entity
            self.set_x(xmlnode.getAttributeNS(XML_URI, "x"))
            self.set_y(xmlnode.getAttributeNS(XML_URI, "y"))

            #get the dimentions of the entity
            self.set_height(xmlnode.getAttributeNS(XML_URI, "height"))
            self.set_width(xmlnode.getAttributeNS(XML_URI, "width"))

            #get the visual properties of the entity
            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "linecolor"))
            self.set_linewidth(xmlnode.getAttributeNS(XML_URI, "linewidth"))
            self.set_fillcolor(xmlnode.getAttributeNS(XML_URI, "fillcolor"))

        else: # TODO: terminar de definir las opciones por defecto
            self.set_name("Entidad "+str(Entity.counter))
            self.set_codename("ENTIDAD_"+str(Entity.counter))
            Entity.counter += 1

    def add_attribute(self, attribute):
        "Agrega un atributo a la entidad"

        for attr in self._attributes_list:
            if (attr.get_codename() == attribute.get_codename()):
                log.debug("Trying to add an attribute with a codename that already exists")
                return False

        self._attributes_list.append(attribute)
        return True

    def del_attribute(self, codename):
        "Elimina un attribute basandose en su codename"

        for i in range(len(self._attributes_list)):
            if (self._attributes_list[i].get_codename() == codename):
                del self._attributes_list[i]
                return True
        else:
            return False

    def to_xml(self, doc, uri):
        "Transforma la información que almacena el objeto en un nodo xml y lo retorna"

        entity = doc.createElementNS(uri, "entity")

        entity.setAttributeNS(uri, "name", self.get_name())
        entity.setAttributeNS(uri, "codename", self.get_codename())
        entity.setAttributeNS(uri, "description", self.get_description())

        entity.setAttributeNS(uri, "x", self.get_x())
        entity.setAttributeNS(uri, "y", self.get_y())

        entity.setAttributeNS(uri, "height", self.get_height())
        entity.setAttributeNS(uri, "width", self.get_width())

        entity.setAttributeNS(uri, "linecolor", self.get_linecolor())
        entity.setAttributeNS(uri, "linewidth", self.get_linewidth())
        entity.setAttributeNS(uri, "fillcolor", self.get_fillcolor())

        for i in range(len(self._attributes_list)):
            log.debug("to xml %s.%s", self.get_codename(),
                      self._attributes_list[i].get_codename())
            attrnode = self._attributes_list[i].to_xml(doc, uri)
            entity.appendChild(attrnode)

        return entity

class Attribute(LogicalBase):
    def __init__(self, xmlnode=None):
        log.debug("Constructing an Attribute")
        LogicalBase.__init__(self)
        self._primary_key = False
        self._data_type = LogicalDataType.INTEGER
        self._data_type_length = None
        self._default_value = None
        self._mandatory = False

        if ((xmlnode != None) and (xmlnode.nodeType == xmlnode.ELEMENT_NODE)):
            self.set_name(xmlnode.getAttributeNS(XML_URI, "name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "description"))

            self.set_primary_key(xmlnode.getAttributeNS(XML_URI, "pk"))
            self.set_data_type(xmlnode.getAttributeNS(XML_URI, "datatype"))
            self._data_type_length = xmlnode.getAttributeNS(XML_URI,
                                                            "datatypelength")
            self.set_default_value(xmlnode.getAttributeNS(XML_URI, "defaultvalue"))
            self.set_mandatory(xmlnode.getAttributeNS(XML_URI, "mandatory"))



    def set_primary_key(self, value):
        self._primary_key = value

    def is_primary_key(self):
        return self._primary_key

    def set_default_value(self, value):
        self._default_value = value

    def get_default_value(self):
        return self._default_value

    def set_data_type(self, datatype, length=None):
        """Define el tipo de dato (datatype) del atributo

        El parametro opcional length se utiliza para definir el largo del tipo
        de dato (se utiliza solamente para los datatype que soportan dicha opcion)

        Por ejemplo:
        VARCHAR(25) => set_datatype(datatype=LogicalDataType.VARCHAR, length=25)

        """
        self._data_type = int(datatype)

        #TODO: es necesario revisar si el tipo de dato soporta la opcion length
        # y solamente setearla cuando corresponde
        if length != None:
            self._data_type_length = str(length)

    def get_data_type(self):
        return self._data_type

    def set_mandatory(self, value):
        self._mandatory = bool(value)

    def is_mandatory(self):
        return self._mandatory


class Relationship(LogicalBase):

    CARDINALITY_1_1 = 0
    CARDINALITY_1_N = 1
    CARDINALITY_N_1 = 2
    CARDINALITY_N_N = 3

    def __init__(self, entity1=None, entity2=None, xmlnode=None, model=None):
        LogicalBase.__init__(self)
        self._cardinality = Relationship.CARDINALITY_1_N
        self._entity1 = entity1
        self._entity2 = entity2

        if ((xmlnode != None) and (model != None)):
            self.set_name(xmlnode.getAttributeNS(XML_URI, "name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "description"))

            self._cardinality = int(xmlnode.getAttributeNS(XML_URI, "cardinality"))
            self._entity1 = model.get_entity(xmlnode.getAttributeNS(XML_URI, "entity1"))
            self._entity2 = model.get_entity(xmlnode.getAttributeNS(XML_URI, "entity2"))

            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "linecolor"))

        elif (entity1 != None) and (entity2 != None):
            config = ConfigurationManager()
            self._linecolor = config.get_relationship_color()

        else:
            log.debug("Trying to construct a relationship without giving the right arguments")
            raise RuntimeError

    def set_cardinality(self, value):
        """Define la cardinalidad de la relacion.

        Usar las constantes Relationship.CARDINALITY_*

        """
        self._cardinality = int(value)

    def get_cardinality(self):
        return self._cardinality

    def set_entity1(self, entity):
        if not isinstance(entity, Entity):
            raise RuntimeError, "Trying to add an object that it is not one"

        self._entity1 = entity

    def get_entity1(self):
        return self._entity1

    def set_entity2(self, entity):
        if not isinstance(entity, Entity):
            raise RuntimeError, "Trying to add an object that it is not one"

        self._entity2

    def get_entity2(self):
        return self._entity2

    def set_linecolor(self, value):
        self._linecolor = value

class Inheritance(LogicalBase):
    counter = 1

    def __init__(self, father=None, son=None, xmlnode=None, model=None):
        self._father = father
        self._son = son

        if (xmlnode != None) and (model != None):

            self.set_name(xmlnode.getAttributeNS(XML_URI, "name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "description"))

            papa = xmlnode.getAttributeNS(XML_URI, "father")
            self.set_father(model.get_entity(papa))
            if self.get_father() != None:
                raise RuntimeError, "When creating an inheritance from a xmlnode \
                could not be located the father entity instance"

            hijo = xmlnode.getAttributeNS(XML_URI, "son")
            self.set_son(model.get_entity(son))
            if self.get_father() != None:
                raise RuntimeError, "When creating an inheritance from a xmlnode \
                could not be located the son entity instance"

            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "linecolor"))

        else:
            config = ConfigurationManager()
            self._linecolor = config.get_inheritance_color()

            self.set_name("Herencia ", str(Inheritance.counter))
            self.set_codename("HERENCIA_", str(Inheritance.counter))
            Inheritance.counter += 1

    def set_father(self, entity):
        "Define la entidad que actua de padre en la herencia"

        if not isinstance(entity, Entity):
            raise RuntimeError, "Trying to add like father an object that is \
            not an instance of Entity"

        self._father = entity

    def get_father(self):
        return self._father

    def set_son(self, entity):
        "Define la entidad que actua de hijo en la herencia"

        if not isinstance(entity, Entity):
            raise RuntimeError, "Trying to add like son an object that is \
            not an instance of Entity"

        self._son = entity

    def get_son(self):
        return self._son

    def set_linecolor(self, value):
        self._linecolor = value

    def get_linecolor(self, value):
        self._linecolor = value


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

    def to_string(cls, type_):
        if type_==LogicalDataType.CHARACTER:
            return "CHARACTER"
        elif type_==LogicalDataType.VARCHAR:
            return "VARCHAR"
        elif type_==LogicalDataType.BIT:
            return "BIT"
        elif type_==LogicalDataType.VARBIT:
            return "VARBIT"
        elif type_==LogicalDataType.NUMERIC:
            return "NUMERIC"
        elif type_==LogicalDataType.DECIMAL:
            return "DECIMAL"
        elif type_==LogicalDataType.INTEGER:
            return "INTEGER"
        elif type_==LogicalDataType.SMALLINT:
            return "SMALLINT"
        elif type_==LogicalDataType.FLOAT:
            return "FLOAT"
        elif type_==LogicalDataType.REAL:
            return "REAL"
        elif type_==LogicalDataType.DOUBLE:
            return "DOUBLE"
        elif type_==LogicalDataType.DATE:
            return "DATE"
        elif type_==LogicalDataType.TIME:
            return "TIME"
        elif type_==LogicalDataType.TIMESTAMP:
            return "TIMESTAMP"
        elif type_==LogicalDataType.INTERVAL:
            return "INTERVAL"

    to_string = classmethod(to_string) #transforma el metodo to_string en estatico

    def get_description(cls, type_):

        #TODO: escribir las descripciones para cada tipo de dato
        if type_==LogicalDataType.CHARACTER:
            return "CHARACTER"
        elif type_==LogicalDataType.VARCHAR:
            return "VARCHAR"
        elif type_==LogicalDataType.BIT:
            return "BIT"
        elif type_==LogicalDataType.VARBIT:
            return "VARBIT"
        elif type_==LogicalDataType.NUMERIC:
            return "NUMERIC"
        elif type_==LogicalDataType.DECIMAL:
            return "DECIMAL"
        elif type_==LogicalDataType.INTEGER:
            return "INTEGER"
        elif type_==LogicalDataType.SMALLINT:
            return "SMALLINT"
        elif type_==LogicalDataType.FLOAT:
            return "FLOAT"
        elif type_==LogicalDataType.REAL:
            return "REAL"
        elif type_==LogicalDataType.DOUBLE:
            return "DOUBLE"
        elif type_==LogicalDataType.DATE:
            return "DATE"
        elif type_==LogicalDataType.TIME:
            return "TIME"
        elif type_==LogicalDataType.TIMESTAMP:
            return "TIMESTAMP"
        elif type_==LogicalDataType.INTERVAL:
            return "INTERVAL"

    get_description = classmethod(get_description)

class Label(RectBase):
    def __init__(self, text=None, xmlnode=None):
        RectBase.__init__(self)
        self._text = text

        if xmlnode != None:
            self._text = xmlnode.getAttributeNS(XML_URI, "text")
            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "linecolor"))
            self.set_linewidth(xmlnode.getAttributeNS(XML_URI, "linewidth"))
            self.set_fillcolor(xmlnode.getAttributeNS(XML_URI, "fillcolor"))
            self.set_width(xmlnode.getAttributeNS(XML_URI, "width"))
            self.set_height(xmlnode.getAttributeNS(XML_URI, "height"))
            self.set_x(xmlnode.getAttributeNS(XML_URI, "x"))
            self.set_y(xmlnode.getAttributeNS(XML_URI, "y"))


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
        log.debug("PhysicalModel.__init__(logicalmodel=%s, path=%s)",
                  logicalmodel, path)

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
