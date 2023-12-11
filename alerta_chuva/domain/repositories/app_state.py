from . import Repository


class AppState:
    """
    Classe responsável por armazenar o estado da aplicação, incluindo o repositório utilizado para acessar os dados.

    Atributos:
        _repository (Repository): O repositório utilizado para acessar os dados.

    Métodos de classe:
        set_repository(repository: Repository) -> None:
            Define o repositório a ser utilizado pela aplicação.

        get_repository() -> Repository:
            Retorna o repositório utilizado pela aplicação.

    Raises:
        TypeError: Caso o repositório não tenha sido definido antes de chamar o método `get_repository`.

    """
    _repository: Repository = None

    @classmethod
    def set_repository(cls, repository: Repository):
        """
        Define o repositório a ser utilizado pela aplicação.

        Args:
            repository (Repository): O repositório a ser definido.

        Returns:
            None

        """
        cls._repository = repository

    @classmethod
    def get_repository(cls) -> Repository:
        """
        Retorna o repositório utilizado pela aplicação.

        Returns:
            Repository: O repositório utilizado pela aplicação.

        Raises:
            TypeError: Caso o repositório não tenha sido definido antes de chamar este método.

        """
        if not cls._repository:
            raise TypeError
        return cls._repository