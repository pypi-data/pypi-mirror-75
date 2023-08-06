#!/usr/bin/env python
# -*- coding: utf-8 -*0


"""A formatter from int to bit size or byte size expression."""


class BinarySizeFormatter:
    """Easily make number for binary size into eye-friendly string.

    Instantiate with number and
    call methods::

        x = zobepy.BinarySizeFormatter(123)
        print(x.get())
        # output string: 123 B
        print(x)
        # output string: 123 B

    Use default
    automatically chosen unit::

        x = zobepy.BinarySizeFormatter(12300)

        print(x.get())
        # output string: 12 KiB
        print(x.get_unit_string())
        # output string: KiB

    .. csv-table:: examples
        :header: "integer value", "converted text (default)"
        :widths: 5, 5

        123, "123 B"
        12300, "12 KiB"
        123000000, "117 MiB"
        1230000000000, "1.1 TiB"
        123000000000000000000000000, "102 YiB"
        12300000000000000000000000000000, "10,174,322 YiB"


    Note:
        The symbols and names are declared in
        IEC 60027-2 A.2 and ISO/IEC 80000.

        Reference: https://en.wikipedia.org/wiki/Binary_prefix

    Parameters
    ----------
    val : int
        An int value.

    """

    def __init__(self, val: int):
        """Initialize this instance."""
        self._val = val
        self._decide_preferred_unit()

    UNIT_B = 0
    """Unit 'bytes'. """

    UNIT_KIB = 1
    """Unit 'kibi bytes', 'KiB'"""

    UNIT_MIB = 2
    """Unit 'mebi bytes', 'MiB'"""

    UNIT_GIB = 3
    """Unit 'gibi bytes', 'GiB'"""

    UNIT_TIB = 4
    """Unit 'tebi bytes', 'TiB'"""

    UNIT_PIB = 5
    """Unit 'pebi bytes', 'PiB'"""

    UNIT_EIB = 6
    """Unit 'exbi bytes', 'EiB'"""

    UNIT_ZIB = 7
    """Unit 'zebi bytes', 'ZiB'"""

    UNIT_YIB = 8
    """Unit 'yobi bytes', 'YiB'"""

    UNIT_MAX = UNIT_YIB
    """Current largest unit symbol is YiB."""

    UNIT_MIN = UNIT_B
    """No symbol."""

    UNIT_SYMBOLS = {
        0: '',
        1: 'Ki',
        2: 'Mi',
        3: 'Gi',
        4: 'Ti',
        5: 'Pi',
        6: 'Ei',
        7: 'Zi',
        8: 'Yi',
    }
    """Binary prefix symbols declared in ISO/IEC 80000."""

    UNIT_NAMES = {
        0: '',
        1: 'kibi',
        2: 'mebi',
        3: 'gibi',
        4: 'tebi',
        5: 'pebi',
        6: 'exbi',
        7: 'zebi',
        8: 'yobi',
    }
    """Binary prefix names declared in ISO/IEC 80000."""

    UNIT_CUSTOMARY_SYMBOLS = {
        0: '',
        1: 'K',
        2: 'M',
        3: 'G',
        4: 'T',
        5: 'P',
        6: 'E',
        7: 'Z',
        8: 'Y',
    }
    """Customary binary prefixes."""

    UNIT_CUSTOMARY_NAMES = {
        0: '',
        1: 'kilo',
        2: 'mega',
        3: 'giga',
        4: 'tera',
        5: 'peta',
        6: 'exa',
        7: 'zeta',
        8: 'yotta',
    }
    """Customary binary prefix names declared in ISO/IEC 80000."""

    @staticmethod
    def round(val, digit: int = 0):
        """Round specified digit of the val.

        Parameters
        ----------
        val : int
            An int value.
        digit : int, default 0
            The digit to be rounded at.

        Returns
        -------
        float
            Rounded value.

        """
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p

    @staticmethod
    def format(val: int) -> str:
        """Easily make number for bytes into eye-friendly string.

        The most simple way to use this class.

        Parameters
        ----------
        val : int
            An int value.

        Returns
        -------
        int
            Formatted string.

        """
        return str(BinarySizeFormatter(val))

    @staticmethod
    def format_base1000(val: int) -> str:
        """Easily make number for bytes into eye-friendly string.

        The most simple way to use this class.

        Unlike format(), this method treats val as decimal.
        ex. format() formats 1024 into 1 KiB
        ex. format_base1000() formats 1000 into 1 KB

        Parameters
        ----------
        val : int
            An int value.

        Returns
        -------
        int
            Formatted string.

        """
        return BinarySizeFormatter(val).get_base1000()

    def __str__(self):
        """Convert value into string with appropriate unit prefix."""
        return self.get()
        # return self.get_value_string() + ' ' + self.get_unit_string()

    def get(self, base1024: int = -1) -> str:
        """Convert value into string. You can choose unit prefix.

        .. csv-table::
            :header: "base1024", "description"

            -1, "default, unit prefix automatically selected"
            0, "expression in bytes. ex. 123: 123 B"
            1, "expression in KiB. ex. 1024: 1.0 KiB"
            2, "expression in MiB."
            "...", "..."
            8, "expression in YiB."

        Parameters
        ----------
        base1024 : int, default -1
            Force the unit.

        Returns
        -------
        str
            Formatted string of the value.

        See also
        --------
        get_value_string : get formatted string of numeric part only

        """
        return (self.get_value_string(base1024)
                + ' ' + self.get_unit_string(base1024))

    def get_base1000(self, base1000: int = -1) -> str:
        """Convert value into string. You can choose unit prefix.

        Unlike get(), this method calculates by decimal.
        ex. get() for int 1024: 1 KiB
        ex. get_base1000() for int 1000: 1 KB

        .. csv-table::
            :header: "base1000", "description"

            -1, "default, unit prefix automatically selected"
            0, "expression in bytes. ex. 123: 123 B"
            1, "expression in KB. ex. 1000: 1.0 KiB"
            2, "expression in MB."
            "...", "..."
            8, "expression in YB."

        Parameters
        ----------
        base1000 : int, default -1
            Force the unit.

        Returns
        -------
        str
            Formatted string of the value.

        See also
        --------
        get_value_string_base1000 : get formatted string of numeric part only

        """
        return (self.get_value_string_base1000(base1000)
                + ' ' + self.get_unit_string_base1000(base1000))

    def get_value_string(self, base1024: int = -1) -> str:
        """Convert numeric value into string.

        Returns number only.
        You can also use unit string getter methods.

        Parameters
        ----------
        base1024 : int, default -1
            Force the unit.
            Set 1 to force the unit 'KiB'.
            Set 2 to force the unit 'MiB'.
            Set 0 to force the unit none.
            Set -1 (default) to automatic.

        Returns
        -------
        str
            Formatted string of the numeric part of the value.

        See also
        --------
        get_unit_string : Like 'KiB', 'MiB'.
        get_unit_symbol : Like 'Ki', 'Mi'.
        get_unit_name : Like 'kibi', 'mebi'.
        get_unit_customary_symbol : Like 'K', 'M'.
        get_unit_customary_name : Like 'kilo', 'mega'.

        """
        if base1024 == -1:
            base1024 = self._unit

        if base1024 == 0:
            s = '{:,}'
            s = s.format(self._val)
            return s
        else:
            if self._val < (100 * (1024 ** (base1024 - 1))):
                return '0.0'
            elif self._val < (10 * (1024 ** base1024)):
                v = self._val / 1024 ** base1024
                v = BinarySizeFormatter.round(v, 1)
                return str(v)
            elif self._val < (100 * (1024 ** base1024)):
                v = self._val / 1024 ** base1024
                v = BinarySizeFormatter.round(v)
                v = int(v)
                return str(v)
            else:
                v = self._val / 1024 ** base1024
                v = BinarySizeFormatter.round(v)
                v = int(v)
                return '{:,}'.format(v)

    def get_value_string_base1000(self, base1000: int = -1) -> str:
        """Convert numeric value into string.

        Returns number only.
        You can also use unit string getter methods.

        Attention
        ---------
        Unlike get_value_string(), this method treats the value decimal(base 10).
        Unlike get_value_string() treats 1024 = 1 KiB,
        this method treats 1000 = 1 KB.
        It is convenient and correct for hard drive vendors.


        Parameters
        ----------
        base1000 : int, default -1
            Force the unit.
            Set 1 to force the unit 'KB'.
            Set 2 to force the unit 'MB'.
            Set 0 to force the unit none.
            Set -1 (default) to automatic.

        Returns
        -------
        str
            Formatted string of the numeric part of the value.

        See also
        --------
        get_unit_string : Like 'KiB', 'MiB'.
        get_unit_symbol : Like 'Ki', 'Mi'.
        get_unit_name : Like 'kibi', 'mebi'.
        get_unit_customary_symbol : Like 'K', 'M'.
        get_unit_customary_name : Like 'kilo', 'mega'.

        """
        if base1000 == -1:
            base1000 = self._unit

        if base1000 == 0:
            s = '{:,}'
            s = s.format(self._val)
            return s
        else:
            if self._val < (100 * (1000 ** (base1000 - 1))):
                return '0.0'
            elif self._val < (10 * (1000 ** base1000)):
                v = self._val / 1000 ** base1000
                v = BinarySizeFormatter.round(v, 1)
                return str(v)
            elif self._val < (100 * (1000 ** base1000)):
                v = self._val / 1000 ** base1000
                v = BinarySizeFormatter.round(v)
                v = int(v)
                return str(v)
            else:
                v = self._val / 1000 ** base1000
                v = BinarySizeFormatter.round(v)
                v = int(v)
                return '{:,}'.format(v)

    def get_unit(self) -> int:
        """Return preferred unit number, in BinarySizeFormatter.UNIT_* constants.

        * Same as base-1024 value.
        * ex. KiB = 1
        * ex. MiB = 2

        Returns
        -------
        int

        """
        return self._unit

    def get_unit_base1000(self) -> int:
        """Return preferred unit number, in BinarySizeFormatter.UNIT_* constants.

        * Same as base-1000 value.
        * ex. KB = 1
        * ex. MB = 2

        Returns
        -------
        int

        """
        return self._unit_base1000

    def get_unit_string(self, base1024: int = -1):
        """Return unit string, KiB, MiB, etc.

        if base1024 = 0, it returns 'B' (no prefix).

        Returns
        -------
        string

        """
        return self.get_unit_symbol(base1024) + 'B'

    def get_unit_string_base1000(self, base1000: int = -1):
        """Return unit string, KB, MB, etc.

        if base1000 = 0, it returns 'B' (no prefix).

        Returns
        -------
        string

        """
        return self.get_unit_customary_symbol(base1000) + 'B'

    def get_unit_symbol(self, base1024: int = -1):
        """Return binary prefix of ISO/IEC 80000. ex:'Ki' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'Ki' (kibi)
        * ex3. 2 = 'Mi' (mebi)

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < BinarySizeFormatter.UNIT_MIN:
            unit = BinarySizeFormatter.UNIT_MIN
        elif unit > BinarySizeFormatter.UNIT_MAX:
            unit = BinarySizeFormatter.UNIT_MAX

        return BinarySizeFormatter.UNIT_SYMBOLS.get(unit, '')

    def get_unit_name(self, base1024: int = -1):
        """Return binary prefix name instead of the symbol. ex:'kibi' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'kibi'
        * ex3. 2 = 'mebi'

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < BinarySizeFormatter.UNIT_MIN:
            unit = BinarySizeFormatter.UNIT_MIN
        elif unit > BinarySizeFormatter.UNIT_MAX:
            unit = BinarySizeFormatter.UNIT_MAX

        return BinarySizeFormatter.UNIT_NAMES.get(unit, '')

    def get_unit_customary_symbol(self, base1024: int = -1):
        """Return customary binary prefix. ex: 'K' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'K' (prefix of 'kilo-bytes' instead of 'kibi')
        * ex3. 2 = 'M' (prefix of 'mega-bytes' instead of 'mebi')

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < BinarySizeFormatter.UNIT_MIN:
            unit = BinarySizeFormatter.UNIT_MIN
        elif unit > BinarySizeFormatter.UNIT_MAX:
            unit = BinarySizeFormatter.UNIT_MAX

        return BinarySizeFormatter.UNIT_CUSTOMARY_SYMBOLS.get(unit, '')

    def get_unit_customary_name(self, base1024: int = -1):
        """Return customary binary prefix name. ex:'kilo' for 1024.

        * ex1. 0 = '' (no prefix)
        * ex2. 1 = 'kilo'
        * ex3. 2 = 'mega'

        If do not specify base1024, it returns automatically preferred prefix
        for the initial value of the instance.

        Returns
        -------
        string

        """
        unit = base1024
        if base1024 == -1:
            unit = self.get_unit()

        if unit < BinarySizeFormatter.UNIT_MIN:
            unit = BinarySizeFormatter.UNIT_MIN
        elif unit > BinarySizeFormatter.UNIT_MAX:
            unit = BinarySizeFormatter.UNIT_MAX

        return BinarySizeFormatter.UNIT_CUSTOMARY_NAMES.get(unit, '')

    def _decide_preferred_unit(self):
        self._unit = BinarySizeFormatter.UNIT_MAX
        for i in range(0, 1 + BinarySizeFormatter.UNIT_MAX):
            if self._val < 512 * (1024**i):
                self._unit = i
                break
        for i in range(0, 1 + BinarySizeFormatter.UNIT_MAX):
            if self._val < 500 * (1000**i):
                self._unit_base1000 = i
                break
