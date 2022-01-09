# -*- coding: utf-8 -*-
"""
                       Paquete fundamentos
  Conjunto de módulos para hacer entrada/salida sencilla en Python

                       Copyright (C) 2019
                 Universidad de Cantabria, SPAIN
                         Versión 1.1
                         Marzo 2019

 @author: Michael Gonzalez   <mgh@unican.es>

 Licencia: GPL
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public
 License as published by the Free Software Foundation; either
 version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

"""



from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import E
from tkinter import SUNKEN
from tkinter import StringVar
from tkinter.ttk import Combobox, Checkbutton, Radiobutton

import time
import math

from typing import List
from typing import Dict

from read_parameters.mensaje import Mensaje
from read_parameters.tooltip import *

class Lectura():
    """
    Esta clase representa una ventana con entradas para teclear datos
    """

    def __init__(self, titulo: str):
        """
        Crea la ventana

        Args:
            titulo: El título de la ventana
        """
        self.__raiz = Tk()
        self.__raiz.title(titulo)
        self.__raiz.resizable(0, 0)

        # contenedores para las entradas
        self.__etiquetas: List[Label] = []
        self.__entradas: List[Label] = []
        self.__textos: List[str] = []
        self.__diccionario: Dict[str, Entry] = {}

        self.__marco = Frame(self.__raiz, borderwidth=2,
                             relief="raised")
        self.__separador = Frame(self.__marco, height=2, bd=1, relief=SUNKEN)
        self.__boton_ok = Button(self.__marco, text="OK",
                                 command=self._on_ok)

        self.__marco.grid(column=0, row=0, padx=5, pady=5)

        self._colocar_widgets()

        self.__finalize = False
        self.__terminate = False
        self.__raiz.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.__raiz.wm_attributes("-topmost", True)
        self.__raiz.update()
        self.__raiz.wm_attributes("-topmost", False)


    def _on_ok(self):
        """
        Anotar que la ventana debe cerrarse
        """
        self.__finalize = True

    def _on_closing(self):
        """
        Destruir la ventana y salir de la aplicación
        """
        self.__finalize = True
        self.__terminate = True
        self.__raiz.quit()
        self.__raiz.destroy()

    def _colocar_widgets(self):
        fila: int = 0
        for i in range(len(self.__textos)):
            self.__etiquetas[i].grid(column=0, row=fila, sticky=E,
                                     padx=5, pady=5)
            self.__entradas[i].grid(column=1, row=fila, padx=5, pady=5)
            fila += 1
        self.__separador.grid(column=0, row=fila,
                              columnspan=2, padx=5, pady=2)
        fila += 1
        self.__boton_ok.grid(column=0, row=fila,
                             columnspan=2, padx=5, pady=5)

    def coloca_widget_donde_quiera(self, entrada, clmn, rw):
        entrada.grid(column=clmn, row=rw, padx=5, pady=5)
        
    def coloca_widget_donde_quiera_special_last_item(self, entrada, clmn, rw, etiqueta):
        self.__etiquetas[0].grid(column=clmn-1, row=rw, sticky=E,
                                     padx=5, pady=5)
        entrada.grid(column=clmn, row=rw, padx=5, pady=5)
        self.__boton_ok.grid(column=0, row=2,
                             columnspan=2, padx=5, pady=5)
        
    def _muestra_error(self, texto: str):
        """
        Muestra un mensaje de error en pantalla

        Args:
            texto: el texto del mensaje de error
        """
        self.__raiz.withdraw()
        msg = Mensaje("Error", texto)
        msg.espera()
        msg.destruye()
        self.__raiz.update()
        self.__raiz.deiconify()


    def crea_entrada(self, msg, etiqueta: str, valor_inicial: str = "", default=True, clmn=0, rw=0, wdth=20):
        """
        Crea una entrada en la que se puede teclear texto

        Args:
            etiqueta: texto colocado al lado de la entrada para identificarla
            valor_inicial: el valor inicial escrito en la entrada
        """
        # Comprobamos etiqueta repetida
        if etiqueta in self.__diccionario:
            self._muestra_error("Etiqueta '"+etiqueta+"' repetida")
            
        if not default:            
            entrada = Entry(self.__marco,
                            textvariable=self.__textos[len(self.__textos)-1],
                            width=wdth)
            self.__entradas.append(entrada)
            entrada.insert(0, valor_inicial)
            self.__diccionario[etiqueta] = entrada
            self.coloca_widget_donde_quiera(entrada, clmn, rw)
            self.escribe_mensaje(msg, entrada)
            
        else:
            lbl = Label(self.__marco, text=etiqueta)
            self.__etiquetas.append(lbl)
            self.__textos.append("")
            entrada = Entry(self.__marco,
                            textvariable=self.__textos[len(self.__textos)-1],
                            width=wdth)
            self.__entradas.append(entrada)
            entrada.insert(0, valor_inicial)
            self.__diccionario[etiqueta] = entrada
            self._colocar_widgets()
            self.escribe_mensaje(msg, lbl)
            
    def crea_label(self, etiqueta, columna, fila):
        Label(self.__marco, text=etiqueta).grid(column=columna, row=fila, padx=5, pady=5)
            
                
            
    def crea_combo(self, msg, etiqueta, values, default=True, clmn=0, rw=0, wdth=20, last=False):
        if etiqueta in self.__diccionario and default:
            self._muestra_error("Etiqueta '"+etiqueta+"' repetida")
            
            
        if not default:

            entrada = Combobox(self.__marco,
                                width=wdth)
            entrada['values'] = values
            entrada['state'] = 'readonly'
            entrada.current(0)
    
            self.__entradas.append(entrada)
            self.__diccionario[etiqueta] = entrada
            
            self.coloca_widget_donde_quiera(entrada, clmn, rw)
            self.escribe_mensaje(msg, entrada)
        else:

            lbl = Label(self.__marco, text=etiqueta)
            self.__etiquetas.append(lbl)
            self.__textos.append("")
            entrada = Combobox(self.__marco,
                                width=wdth)
            entrada['values'] = values
            entrada['state'] = 'readonly'
            entrada.current(0)

            self.__entradas.append(entrada)
            self.__diccionario[etiqueta] = entrada
            if last:
                self.coloca_widget_donde_quiera_special_last_item(entrada, clmn, rw, etiqueta)
            else:
                self._colocar_widgets()
            self.escribe_mensaje(msg, lbl)
        return entrada
       
    def espera(self)-> bool:
        """
        Pinta la ventana y espera hasta que se pulsa OK

        Returns:
            True si se ha matado la ventana, False si se ha pulsado OK
        """
        self.__raiz.update()
        while not self.__finalize:
            self.__raiz.update()
            time.sleep(0.01)
        self.__finalize = False
        return self.__terminate


    def lee_string(self, etiqueta: str) -> str:
        """
        Lee el texto de la entrada cuya etiqueta se indica

        Si la entrada no existe se pone un mensaje de error

        Args:
            etiqueta: la etiqueta de la entrada que se desea leer
        Returns:
            el texto escrito en la entrada deseada, si existe, o un
            string vacío si la entrada no existe
        """
        if etiqueta in self.__diccionario:
            return self.__diccionario[etiqueta].get().lower()
        # La etiqueta no existe
        self._muestra_error("Etiqueta '"+etiqueta+"' no existe")
        return ""


    def lee_int(self, etiqueta: str) -> str:
        """
        Lee el número entero de la entrada cuya etiqueta se indica. Si el numero
        no es entero devuelve el entero más cercano

        Si la entrada no existe se pone un mensaje de error y retorna -1

        Args:
            etiqueta: la etiqueta de la entrada que se desea leer
        Returns:
            el número entero escrito en la entrada deseada, si existe, o -1
            si la entrada no existe o es incorrecta
        """
        num: str = self.lee_string(etiqueta)
        if num == "":
            return -1
        
        return int(num)
    

    def lee_float(self, etiqueta: str) -> str:
        """
        Lee el número real de la entrada cuya etiqueta se indica

        Si la entrada no existe se pone un mensaje de error y se retorna nan

        Args:
            etiqueta: la etiqueta de la entrada que se desea leer
        Returns:
            el número entero escrito en la entrada deseada, si existe, o nan
            si la entrada no existe o es incorrecta
        """
        num: str = self.lee_string(etiqueta)
        if num == "":
            return math.nan
        
        return float(num)
        
    def escribe_mensaje(self, mensaje, widget):

         CreateToolTip(widget, text=mensaje)


    def destruye(self):
        """
        Destruir la ventana
        """
        if not self.__terminate:
            self.__raiz.quit()
            self.__raiz.destroy()
