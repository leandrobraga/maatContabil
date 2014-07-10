# -*- coding: iso-8859-1 -*-
#Copyright 2012 Leandro Quadros Durães Braga

#Este arquivo é parte do programa Sistema de Controle de Paciente(SCP)
#Sistema de Controle de Paciente(SCP) é um software livre; você pode redistribui-lo e/ou
#modifica-lo dentro dos termos da Licença Pública Geral GNU como
#publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
#Este programa é distribuido na esperança que possa ser  util,
#mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
#Você deve ter recebido uma cópia da Licença Pública Geral GNU
#junto com este programa, se não, escreva para a Fundação do Software
#Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from distutils.core import setup
import py2exe


setup(
      windows=[{"script":"updatedb.py", "icon_resources":[(0x0004,"./imagens/file.ico")]}],


      options={"py2exe":{

            "includes":["sqlite3","sqlalchemy.dialects.sqlite","elixir"],
            "excludes":['_ssl','doctest','optparse','bsddb','compiler',
                        'curses','pickle','calendar','antigravity',
                        'cgi','bz2',
                        ],
            "dll_excludes":["msvcr71.dll","API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
    "POWRPROF.dll",
    "w9xpopen.exe"],
            }}

       
      )