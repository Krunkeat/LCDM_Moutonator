import sys
import os
import PySide2.QtGui as qtg
import csv
import maya.cmds as cmds

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
        
class MyWidget(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(MyWidget, self).__init__(parent)   
        
        self.setWindowTitle('MOUTONNATOR v0.1')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setFixedSize(300, 407)
        
        
        self.import_file = r"S:\SIC3D\SIC5\Projects\moutons\04-ASSETS\Main Characters\moutons_A_Mouton\moutons_A_Mouton_Shade\moutons_A_Mouton_Shade.mb"
        
        # Table Widget
        self.table_widget = QtWidgets.QTableWidget(parent=self)
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(["Variation"])
        self.table_widget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table_widget.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        self.table_widget.showGrid()
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        #set value
        #
        #  ["BODY", "LAINE", "EYES", "DENTS"]
        variation_dict = {
        1: ["Hair_Shader_Fuzz_SHD_Mouton_Var1_Body", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        2: ["Hair_Shader_Fuzz_SHD_Mouton_BICOLOR_Body", "Hair_Shader_Fuzz_SHD_Mouton_Var2_Wool", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        3: ["Hair_Shader_Fuzz_SHD_Mouton_EMOVar01_Body", "Hair_Shader_Fuzz_SHD_Mouton_EMOVar01_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        4: ["Hair_Shader_Fuzz_SHD_Mouton_EMOVar02_Body", "Hair_Shader_Fuzz_SHD_Mouton_EMOVar02_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        5: ["Hair_Shader_Fuzz_SHD_Mouton_EMOVar03_Body", "Hair_Shader_Fuzz_SHD_Mouton_EMOVar03_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        6: ["Hair_Shader_Fuzz_SHD_Mouton_EMOVar04_Body", "Hair_Shader_Fuzz_SHD_Mouton_EMOVar04_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        7: ["Hair_Shader_Fuzz_SHD_Mouton_BALDVar01_Body", "Hair_Shader_Fuzz_SHD_Mouton_BALDVar01_Laine", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        8: ["Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar03_Body", "Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar03_Laine", "Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar03_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"],
        9: ["Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar04_Body", "Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar04_laine", "Hair_Shader_Fuzz_SHD_Mouton_FrizzyVar04_Eyes", "Hair_Shader_Fuzz_SHD_Mouton_Var1_Dents"]
        }
        
        for var in variation_dict:
            rowPosition = self.table_widget.rowCount()
            self.table_widget.insertRow(rowPosition)
            var_name = variation_dict[var][0].split("_")[-2]
            table_value = QtWidgets.QTableWidgetItem(f"Variation_{var:02d}  {var_name}")
            table_value.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            table_value.setData(QtCore.Qt.UserRole, variation_dict[var])
            self.table_widget.setItem(rowPosition, 0, table_value)
            
        # Assign btn
        self.assign_btn = QtWidgets.QPushButton("Assign")
        self.assign_fuzz_btn = QtWidgets.QPushButton("Assign Fuzz")
        #Warning
        self.warn = QtWidgets.QLabel(" Select first the Standin, then the Mesh ")
        self.warn.setStyleSheet(f"color: {QtGui.QColor(250, 250, 250).name()}; background-color: {QtGui.QColor(200, 75, 75).name()};"
                                f" padding: 6px;"
                                f" font: bold 12px;"
                                f" border-style: solid;"
                                f" border-width: 2px;"
                                f" border-radius: 10px;"
                                f"border-color: {QtGui.QColor(100, 50, 50).name()}")
        
        #
        #  Layout
        #
        
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(4, 4, 4, 4)
        
        
        self.mainLayout.addWidget(self.table_widget)
        self.mainLayout.addWidget(self.assign_btn)
        self.mainLayout.addWidget(self.warn)
        self.mainLayout.addWidget(self.assign_fuzz_btn)
        
        
        # Connect event
        self.assign_btn.clicked.connect(self.assign_btn_on_clicked)  
        self.assign_fuzz_btn.clicked.connect(self.assign_fuzz_btn_on_clicked)
        
    #
    # Fctn
    #
    def getSGfromShader(self, shader=None):
        if shader:
            if cmds.objExists(shader):
                sgq = cmds.listConnections(shader, d=True, et=True, t='shadingEngine')
                if sgq:
                    return sgq[0]
    
        return None

    def assignObjectListToShader(self, objList=None, shader=None):
        """
        Assign the shader to the object list
        arguments:
            objList: list of objects or faces
        """
        # assign selection to the shader
        shaderSG = self.getSGfromShader(shader)
        if objList:
            if shaderSG:
                cmds.sets(objList, e=True, forceElement=shaderSG)
            else:
                print('The provided shader didn\'t returned a shaderSG')
        else:
            print('Please select one or more objects')
    
    def getSHDfromObj(self, obj):
        """
        Get the Shader connected to the obj
        """
        shape = maya.cmds.listRelatives ( obj, shapes=True, f=True)[0]
        shadingEngine = maya.cmds.listConnections (shape, source=False, destination=True)
        material = maya.cmds.listConnections (shadingEngine, source=True, destination=False)
        attr = shadingEngine[0]+'.surfaceShader'
        shd = maya.cmds.connectionInfo( attr, sourceFromDestination=True).split(".")[0]
        
        return shd
    
    def assign_btn_on_clicked(self):
        """ 
            Assign Texture of selected varition

        """
        indexes = self.table_widget.selectionModel().selectedRows()
        for index in sorted(indexes):
            table_value = self.table_widget.item(index.row(), 0).data(QtCore.Qt.UserRole)
            var_num = index.row()+1
            print(f'Variation_{var_num:02d} is selected')
            
            sel = cmds.ls(sl=True)
            #import if not
            imp= True
            
            if cmds.objExists("Hair_Shader_Fuzz_SHD_Mouton_Var1_Body"):
                imp = False
                print("already in the scene skiped import for now, import it by hand if needed")
            
            if imp:
                cmds.file(self.import_file, i=True ,type="mayaBinary" ,ra=True ,rdn=True ,mergeNamespacesOnClash=False ,rpr="Hair_Shader_Fuzz" ,options="v=0;" )
                cmds.delete(f"Hair_Shader_Fuzz_grp_all")

            #Assign
            x = cmds.listRelatives(sel,ad=True,f=True)
            for index,grp in enumerate(["BODY_grp","HAIR_msh_grp","EYES_msh_grp","TEETH_grp"]):
                for doss in x:
                    if grp in doss:
                        shd = table_value[index]
                        self.assignObjectListToShader(doss,shd)
                        


    
    
    def assign_fuzz_btn_on_clicked(self):
        sel = cmds.ls(sl=True)
        standin = sel[0]
        msh = sel[1]
        
        
        # get shader connected to the msh
        shd = self.getSHDfromObj(msh)
        basecolo = maya.cmds.connectionInfo( shd+".baseColor", sourceFromDestination=True)
        fName = basecolo.split('.')[0] + ".fileTextureName"
        var = cmds.getAttr(fName).split("/")[-3]
        shd_basic = f"Hair_Shader_{var}_MOUTON_base_FUZZ_HAIR_SHD"
        
        if len(maya.cmds.connectionInfo( basecolo, destinationFromSource=True)) <= 2:
            print("to import")
            if not cmds.objExists(shd_basic):
                cmds.file("S:/SIC3D/SIC5/Projects/moutons/02-PROD/moutons_G_VFX/Mouton_Shader_Fuzz.mb", i=True ,type="mayaBinary" ,ra=True ,rdn=True ,mergeNamespacesOnClash=False ,rpr=f"Hair_Shader_{var}" ,options="v=0;" )
                cmds.delete(f"Hair_Shader_{var}_pSphere4")
            
            cmds.connectAttr(basecolo, shd_basic+".baseColor")
            cmds.connectAttr(basecolo, shd_basic+".diffuseColor")
            
        print("proceed to connect")
        self.assignObjectListToShader(standin , shd_basic)
        
        cmds.setAttr(shd_basic+".diffuse", 0)
    
if __name__ == "__main__":
    try:
        ui.deleteLater()
    except:
        pass
    ui = MyWidget()

    try:
        ui.show()
    except:
        ui.deleteLater()
