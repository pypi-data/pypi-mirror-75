from typing import Dict, List, Optional


class Context:
    """
    An API class for handling input and output contexts.

    This class allows to create, edit or delete contexts during conversations.

    Parameters:
        input_contexts (List[Dict]): The contexts that were active in the
            conversation when the intent was triggered by Dialogflow.
        session (str): The session of the conversation.

    Attributes:
        input_contexts (List[Dict]): The contexts that were active in the
            conversation when the intent was triggered by Dialogflow.
        session (str): The session of the conversation.
        contexts (Dict[str, Dict]): A mapping of context names to context
            objects (dictionaries).
    """

    def __init__(self, input_contexts: List[Dict], session: str) -> None:
        self._index = None
        self._context_array = None

        self.input_contexts = self._process_input_contexts(input_contexts)
        self.session = session
        self.contexts = self._process_input_contexts(input_contexts)

    @staticmethod
    def _process_input_contexts(input_contexts) -> Dict[str, Dict]:
        """Processes a list of Dialogflow input contexts"""
        contexts = {}

        for context in input_contexts:
            name = context['name'].rsplit('/', 1)[-1]
            context['name'] = name
            contexts[name] = context

        return contexts

    def set(self, name: str, lifespan_count: Optional[int] = None, parameters: Optional[Dict] = None) -> None:
        """
        Sets the lifepan and parameters of a context (if the context exists) or
        creates a new output context (if the context doesn't exist).

        Parameters:
            name (str): The name of the context.
            lifespan_count (Optional[int]): The lifespan duration of the
                context (in minutes).
            parameters (Optional[Dict]): The parameters of the context.

        Raises:
            TypeError: `name` argument must be a string
        """
        if not isinstance(name, str):
            raise TypeError('name argument must be a string')

        if name not in self.contexts:
            self.contexts[name] = {'name': name}

        if lifespan_count is not None:
            self.contexts[name]['lifespanCount'] = lifespan_count

        if parameters is not None:
            self.contexts[name]['parameters'] = parameters

    def get(self, name: str) -> Optional[Dict]:
        """
        Finds a context object (dictionary) if exists.

        Parameters:
            name (str): The name of the context.

        Returns:
            Optional[Dict]: The context object (dictionary) if exists.
        """
        return self.contexts.get(name)

    def delete(self, name: str) -> None:
        """
        Deletes a context by setting its lifespan to 0.

        Parameters:
            name (str): The name of the context.
        """
        self.set(name, lifespan_count=0)

    def get_output_contexts_array(self) -> List[Dict]:
        """
        Returns the output contexts as an array.

        Returns:
            List[Dict]: The output contexts (dictionaries).
        """
        output_contexts = [*self]

        for context in output_contexts:
            context['name'] = f"{self.session}/contexts/{context['name']}"

        return output_contexts

    def __iter__(self) -> 'Context':
        self._index = 0
        self._context_array = list(self.contexts.values())

        return self

    def __next__(self) -> Dict:
        if self._index >= len(self._context_array):
            raise StopIteration

        context = self._context_array[self._index]

        self._index += 1

        return context
