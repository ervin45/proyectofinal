#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
#DATABASE_HOST = '192.168.61.102'
DATABASE_HOST = 'localhost'

def cursor():
    import psycopg2
    import psycopg2.extras
    con = psycopg2.connect(host=DATABASE_HOST, port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
    return con.cursor(cursor_factory=psycopg2.extras.DictCursor) #############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
#DATABASE_HOST = '192.168.61.102'
DATABASE_HOST = 'localhost'

def cursor():
    import psycopg2
    import psycopg2.extras
    con = psycopg2.connect(host=DATABASE_HOST, port=5432, user="ncesar", password=".,supermo", database="bieler_dw")
    return con.cursor(cursor_factory=psycopg2.extras.DictCursor) 