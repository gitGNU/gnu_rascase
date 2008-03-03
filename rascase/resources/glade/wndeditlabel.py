##
## wndeditlabel.py
## Login : <freyes@yoda.>
## Started on  Tue Dec 18 19:26:16 2007 Felipe Reyes
## $Id$
## 
## Copyright (C) 2007 Felipe Reyes <felipereyes@gmail.com>
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
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
##


import gobject
import gtk
import gtk.glade


def main():
    wTree = gtk.glade.XML("wndeditlabel.glade")

    win = wTree.get_widget("wndeditlabel")
    win.set_title("Editar Etiqueta")
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()
