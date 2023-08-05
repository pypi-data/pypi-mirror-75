class AccountRequiredParamsError(Exception):
    """Raised when trying to create an account without some required paramether"""

    message = """
    .
    Missing required paramether "{}" to create an account.
    Please make sure all required parameters are provided:
    [corporateName*, documentNumber, documentType, nationality*, email,
    name*, surname*, phone, postalCode, province, region, roadName,
    roadNumber, roadType, town]
    * if appropriate, according to documentType
    """

    def __init__(self, missing_paramether):
        self.message = self.message.format(missing_paramether)
        super().__init__(self.message)
