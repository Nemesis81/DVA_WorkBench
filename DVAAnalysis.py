
import FreeCAD as App
# import PartDesign
# import Part
import FreeCADGui as Gui
import os

TOOL_ICON = os.path.join(App.getUserAppDataDir(),
                         "Mod",
                         "DVA_WorkBench",
                         "ressources",
                         "DVA_Analysis.svg")


class cmd_dvaAnalysis():
    """Add DVA analysis to the document"""

    def GetResources(self):
        return {"Pixmap"  : TOOL_ICON,
                "Accel"   : "Shift+S",
                "MenuText": "Create DVA Analysis",
                "ToolTip" : "Create a DVA Analysis for main parameters"}

    def Activated(self):
        """
        Object creation method
        """

        obj = App.ActiveDocument.addObject('App::DocumentObjectGroup',
                                           "DVA_Analysis")

        dvaAnalysis(obj)
        App.ActiveDocument.recompute()
        return

    def IsActive(self):
        """
        Here you can define if the command must be active
        or not (greyed) if certain conditions
        are met or not. This function is optional.
        """
        return True


class dvaAnalysis():
    def __init__(self, obj):
        """
        Default constructor
        """

        self.Type = 'dvaAnalysis'

        obj.addProperty('App::PropertyEnumeration',
                        'AnalysisType',
                        'DVA',
                        'Analisys type, Monte Carlo or HLM').AnalysisType

        obj.AnalysisType = ["Monte Carlo", "High Low Mean"]
        obj.addProperty("App::PropertyInteger",
                        "Sample",
                        "DVA",
                        "quantity of loop in DVA analysis").Sample

        obj.addProperty('App::PropertyEnumeration',
                        'Cp',
                        'DVA',
                        'Cp level expected').Cp

        obj.Cp = [1, 1.33, 1.67, 2]
        obj.addProperty("App::PropertyFile",
                        "OutputFile",
                        "DVA",
                        "Path of the output file")

        obj.addProperty("App::PropertyStringList",
                        "ListPoints",
                        "DVA",
                        "List of measured point to be ouputed to the file")

    def execute(self, obj):
        """
        Called on document recompute
        """
        App.ActiveDocument.recompute()


class ViewProviderDvaAnalysis:
    def __init__(self, obj):
        """
        Set this object to the proxy object of the actual view provider
        """

        obj.Proxy = self

    def attach(self, obj):
        """
        Setup the scene sub-graph of the view provider,
         this method is mandatory
        """
        return

    def updateData(self, fp, prop):
        """
        If a property of the handled feature has changed we have the chance
        to handle this here
        """
        return

    def getDisplayModes(self, obj):
        """
        Return a list of display modes.
        """
        return []

    def getDefaultDisplayMode(self):
        """
        Return the name of the default display mode.
        It must be defined in getDisplayModes.
        """
        return "Shaded"

    def setDisplayMode(self, mode):
        """
        Map the display mode defined in attach with those defined
        in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        return mode

    def onChanged(self, vp, prop):
        """
        Print the name of the property that has changed
        """

        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def getIcon(self):
        """
        Return the icon in XMP format which will appear in the tree view.
        This method is optional and if not defined a default icon is shown.
        """

        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "    c None",
            ".   c #141010",
            "+   c #615BD2",
            "@   c #C39D55",
            "#   c #000000",
            "$   c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        """
        Called during document saving.
        """
        return None

    def __setstate__(self, state):
        """
        Called during document restore.
        """
        return None


Gui.addCommand("DVA Analisys Creation", cmd_dvaAnalysis())
