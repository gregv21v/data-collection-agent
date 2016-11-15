# Each command has a name, and a list of parameters, and a parameter can either
# be a list or a single string. Lists always are at the end of a command
class Command:



    def __init__(self, cmdString):
        # convert the command into a usable format
        if("\"" in cmdString):
            # convert the command into a usable format
            self.name = cmdString.split(" ")[0]
            self.parameters = []

            quotes = self.getIndicesOf(cmdString, "\"")

            # find string parameters
            quoteIndex = 0
            while(quoteIndex < len(quotes)):
                self.parameters.append(cmdString[quotes[quoteIndex]+1:quotes[quoteIndex+1]]);
                quoteIndex += 2

            # find list parameters
            startBrackets = self.getIndicesOf(cmdString, "{")
            endBrackets = self.getIndicesOf(cmdString, "}")

            for bIndex in range(0, len(startBrackets)):
                self.parameters.append(cmdString[startBrackets[bIndex]+1:endBrackets[bIndex]].split(" "))
        else:
            self.name = cmdString.split(" ")[0]
            self.parameters = cmdString.split(" ")[1:]

    def getIndicesOf(self, cmdString, symbol):
        quotes = []
        index = cmdString.find(symbol)
        while(index > -1):
            quotes.append(index)
            if(cmdString[index+1:].find(symbol) != -1):
                index += cmdString[index+1:].find(symbol) + 1
            else:
                index = -1
        return quotes;
