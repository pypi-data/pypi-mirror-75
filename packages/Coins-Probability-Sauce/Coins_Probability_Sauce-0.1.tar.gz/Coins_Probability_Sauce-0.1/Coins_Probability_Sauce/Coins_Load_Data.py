class CoinsLoadData:

    def __init__(self, A_count=2, B_count=2):
        """Generic coin collection for calculating basic probabilities.

        Attributes:
            A_count (int) representing the number of A coins in a collection.
            B_count (int) representing the number of B coins in a collection.
            n (int) representing the total coins in the collection
            data_list (list of strings) a list of A and B coins representing a coin collection.
            """
        self.A_count = A_count
        self.B_count = B_count
        self.n = A_count + B_count
        self.data = ['A', 'A', 'B', 'B']
