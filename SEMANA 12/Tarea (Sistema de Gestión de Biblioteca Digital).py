#SEMANA 12 (TAREA: SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL)
#NOMBRE: FLOR MUÑOZ

"""
Se realizo el Sistema simple de Gestión de Biblioteca Digital
Esto Cumple con:
- Libro: usa tupla para (titulo, autor)
- Usuario: lista de libros prestados
- Biblioteca: dict para libros por ISBN, set para IDs de usuarios
- Funcionalidades: añadir/quitar libros, registrar/dar de baja usuarios,
  prestar/devolver libros, búsquedas y listar préstamos.
"""

from dataclasses import dataclass, field
from typing import Tuple, Dict, List, Set, Optional


@dataclass(frozen=True)
class Libro:
    """
    Representa un libro.
    - title_author: tupla (titulo, autor) — inmutable por diseño.
    - categoria: cadena (puede cambiar si se necesita, pero lo dejamos simple).
    - isbn: identificador único (clave en catálogo).
    """
    title_author: Tuple[str, str]
    categoria: str
    isbn: str

    @property
    def titulo(self) -> str:
        return self.title_author[0]

    @property
    def autor(self) -> str:
        return self.title_author[1]

    def __str__(self):
        return f"{self.titulo} — {self.autor} (ISBN: {self.isbn}, Cat: {self.categoria})"


@dataclass
class Usuario:
    """
    Representa un usuario de la biblioteca.
    - nombre: nombre del usuario.
    - user_id: identificador único (debe gestionarlo Biblioteca).
    - prestados: lista de ISBNs de libros actualmente prestados a este usuario.
    """
    nombre: str
    user_id: str
    prestados: List[str] = field(default_factory=list)

    def prestar(self, isbn: str) -> None:
        """Añade ISBN a la lista de prestados (no verifica aquí disponibilidad)."""
        self.prestados.append(isbn)

    def devolver(self, isbn: str) -> bool:
        """Quita ISBN de la lista de prestados; devuelve True si estaba y se quitó."""
        if isbn in self.prestados:
            self.prestados.remove(isbn)
            return True
        return False

    def listar_prestados(self) -> List[str]:
        return list(self.prestados)

    def __str__(self):
        return f"{self.nombre} (ID: {self.user_id}) - Prestados: {len(self.prestados)}"


class Biblioteca:
    """
    Clase que gestiona libros, usuarios y préstamos.
    - libros: dict {isbn: Libro}
    - usuarios: dict {user_id: Usuario}
    - usuarios_ids: set de user_id para garantizar unicidad
    - prestamo_activo: dict {isbn: user_id} para saber qué libro está prestado y a quién
    """

    def __init__(self):
        self.libros: Dict[str, Libro] = {}
        self.usuarios: Dict[str, Usuario] = {}
        self.usuarios_ids: Set[str] = set()
        self.prestamo_activo: Dict[str, str] = {}  # isbn -> user_id

    # ---------- Gestión de libros ----------
    def agregar_libro(self, libro: Libro) -> bool:
        """Agrega libro al catálogo. Devuelve False si ISBN ya existe."""
        if libro.isbn in self.libros:
            return False
        self.libros[libro.isbn] = libro
        return True

    def quitar_libro(self, isbn: str) -> bool:
        """
        Quita libro del catálogo si existe y no está prestado.
        Devuelve True si se eliminó, False si no existe o está prestado.
        """
        if isbn not in self.libros:
            return False
        if isbn in self.prestamo_activo:
            # No permitir borrar libro que está prestado
            return False
        del self.libros[isbn]
        return True

    # ---------- Gestión de usuarios ----------
    def registrar_usuario(self, nombre: str, user_id: str) -> bool:
        """Registra nuevo usuario. Devuelve False si el ID ya existe."""
        if user_id in self.usuarios_ids:
            return False
        usuario = Usuario(nombre=nombre, user_id=user_id)
        self.usuarios[user_id] = usuario
        self.usuarios_ids.add(user_id)
        return True

    def baja_usuario(self, user_id: str) -> bool:
        """
        Da de baja a un usuario. Solo si existe y no tiene libros prestados.
        Devuelve True si se dio de baja.
        """
        usuario = self.usuarios.get(user_id)
        if not usuario:
            return False
        if usuario.prestados:
            # No permitir baja si tiene libros prestados
            return False
        del self.usuarios[user_id]
        self.usuarios_ids.discard(user_id)
        return True

    # ---------- Préstamos ----------
    def prestar_libro(self, isbn: str, user_id: str) -> bool:
        """
        Presta libro identificado por ISBN al usuario user_id.
        Condiciones: libro existe y no esté prestado; usuario registrado.
        Devuelve True si préstamo OK.
        """
        if isbn not in self.libros:
            return False  # no existe el libro
        if isbn in self.prestamo_activo:
            return False  # ya prestado
        if user_id not in self.usuarios_ids:
            return False  # usuario no registrado

        # Registrar préstamo
        self.prestamo_activo[isbn] = user_id
        self.usuarios[user_id].prestar(isbn)
        return True

    def devolver_libro(self, isbn: str, user_id: str) -> bool:
        """
        Devuelve libro: quita el préstamo activo si corresponde.
        Devuelve True si la devolución fue exitosa.
        """
        actual_user = self.prestamo_activo.get(isbn)
        if actual_user != user_id:
            return False  # o libro no prestado o prestado a otro usuario
        # quitar registro
        del self.prestamo_activo[isbn]
        ok = self.usuarios[user_id].devolver(isbn)
        return ok

    # ---------- Búsquedas ----------
    def buscar_por_titulo(self, texto: str) -> List[Libro]:
        texto_l = texto.lower()
        return [lib for lib in self.libros.values() if texto_l in lib.titulo.lower()]

    def buscar_por_autor(self, texto: str) -> List[Libro]:
        texto_l = texto.lower()
        return [lib for lib in self.libros.values() if texto_l in lib.autor.lower()]

    def buscar_por_categoria(self, categoria: str) -> List[Libro]:
        cat_l = categoria.lower()
        return [lib for lib in self.libros.values() if cat_l == lib.categoria.lower()]

    # ---------- Listados ----------
    def listar_todos_libros(self) -> List[Libro]:
        return list(self.libros.values())

    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())

    def listar_prestados_usuario(self, user_id: str) -> Optional[List[Libro]]:
        """Devuelve lista de objetos Libro prestados a user_id, o None si no existe el usuario."""
        usuario = self.usuarios.get(user_id)
        if not usuario:
            return None
        return [self.libros[isbn] for isbn in usuario.prestados if isbn in self.libros]

    def quien_tiene_el_libro(self, isbn: str) -> Optional[Usuario]:
        """Devuelve el Usuario que tiene prestado el libro (o None)."""
        user_id = self.prestamo_activo.get(isbn)
        if user_id:
            return self.usuarios.get(user_id)
        return None

    # ---------- Utilitarios ----------
    def esta_prestado(self, isbn: str) -> bool:
        return isbn in self.prestamo_activo

    def disponible(self, isbn: str) -> bool:
        return (isbn in self.libros) and (isbn not in self.prestamo_activo)


# ------------------ Pruebas de funcionamiento / ejemplo de uso ------------------

def ejemplo_uso():
    bib = Biblioteca()

    # Agregar libros (otros ejemplos)
    b1 = Libro(title_author=("Cien Años de Soledad", "Gabriel García Márquez"),
               categoria="Literatura", isbn="978-0101")
    b2 = Libro(title_author=("Introducción a la Programación", "Ana Torres"),
               categoria="Informática", isbn="978-0102")
    b3 = Libro(title_author=("Historia del Arte Moderno", "Luis Fernández"),
               categoria="Arte", isbn="978-0103")
    b4 = Libro(title_author=("Álgebra Lineal con Aplicaciones", "David Morales"),
               categoria="Matemáticas", isbn="978-0104")

    assert bib.agregar_libro(b1)
    assert bib.agregar_libro(b2)
    assert bib.agregar_libro(b3)
    assert bib.agregar_libro(b4)

    # Registrar usuarios (otros nombres)
    assert bib.registrar_usuario("Valentina Herrera", "U100")
    assert bib.registrar_usuario("Santiago Castro", "U101")
    assert bib.registrar_usuario("Lucía Andrade", "U102")

    # Préstamos
    assert bib.prestar_libro("978-0101", "U100")  # Valentina pide "Cien Años de Soledad"
    assert bib.prestar_libro("978-0102", "U101")  # Santiago pide "Introducción a la Programación"
    assert bib.prestar_libro("978-0103", "U102")  # Lucía pide "Historia del Arte Moderno"

    # Listar libros prestados
    print("Prestados U100:", [str(l) for l in bib.listar_prestados_usuario("U100")])
    print("Prestados U101:", [str(l) for l in bib.listar_prestados_usuario("U101")])
    print("Prestados U102:", [str(l) for l in bib.listar_prestados_usuario("U102")])

    # Devolver libro
    assert bib.devolver_libro("978-0101", "U100")
    print("Valentina devolvió su libro, ahora tiene:", bib.listar_prestados_usuario("U100"))

    # Buscar por autor
    res_autor = bib.buscar_por_autor("Ana Torres")
    print("Búsqueda por autor 'Ana Torres':", [str(l) for l in res_autor])

    # Buscar por categoría
    res_cat = bib.buscar_por_categoria("Matemáticas")
    print("Búsqueda por categoría 'Matemáticas':", [str(l) for l in res_cat])

    # Baja de usuario sin préstamos
    assert bib.baja_usuario("U100")  # Valentina ya devolvió y se puede dar de baja
    print("Usuarios activos:", [str(u) for u in bib.listar_usuarios()])

    print("Todo OK - Ejemplo con nuevos datos completado.")


if __name__ == "__main__":
    ejemplo_uso()
