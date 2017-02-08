# This module imports libraries and such so python can call into the PI system
import numpy as np

import sys
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')

import clr #requires pythonnet
clr.AddReference('OSIsoft.AFSDK')
clr.AddReference('System.Collections')
from System import Object
from System.Collections import *

# This imports the difference AF classes
from OSIsoft.AF.PI import *  
from OSIsoft.AF.Search import *  
from OSIsoft.AF.Asset import *  
from OSIsoft.AF.Data import *  
from OSIsoft.AF.Time import *  

# create the import function for server connection
def Connect_To_Server(serverName):  
    piServers = PIServers()  
    global piServer  
    piServer = piServers[serverName]  
    piServer.Connect(False)  

# create the import function for tag call: get snapshot
def Get_Tag_Snapshot(tagname):  
    tag = PIPoint.FindPIPoint(piServer, tagname)  
    tag_AFValue = tag.Snapshot()  
    return tag_AFValue.Value, tag_AFValue.Timestamp

# create the import function for tag call: read single value
def Get_Tag_Value(tagname, timestamp):
    tag = PIPoint.FindPIPoint(piServer, tagname) 
    tag_AFTime = AFTime(timestamp)
    tag_AFValue = tag.RecordedValue(tag_AFTime,0)
    return tag_AFValue

# create the import function for tag call: multiple values
def Get_Tag_Values(tagname, timestart, timeend):
    tag = PIPoint.FindPIPoint(piServer, tagname) 
    tag_AFTimeRange = AFTimeRange(timestart, timeend)
    tag_Boundary = AFBoundaryType.Inside
    tag_AFValues = tag.RecordedValues(tag_AFTimeRange, tag_Boundary, '', False, 0)
    
    # convert AFValues object into numpy array of values and timestamps
    list_AFValues = list(tag_AFValues)
    array_Values = np.zeros((len(list_AFValues), 1), dtype='object')
    array_Timestamps = np.zeros((len(list_AFValues), 1), dtype='object')
    for i, tag_AFValue in enumerate(tag_AFValues):
        array_Values[i, :] = np.array([float(tag_AFValue.Value)])
        array_Timestamps[i, :] = np.array([str(tag_AFValue.Timestamp)])
        
    # identify the timestamps associated with the first and last data point
    timeend_actual = array_Timestamps[len(array_Timestamps)-1]
    timestart_actual = array_Timestamps[0]
    print 'Number of data points between', timestart, 'and', timeend, '=', len(list_AFValues)
    print ('actual timestart:{0}'.format(timestart_actual))
    print ('actual timeend:{0}'.format(timeend_actual))
    return array_Values, array_Timestamps




#create the import function for tag call: update single value    
def Update_Tag_Value(tagname, value, timestamp):
    tag_Value = clr.System.Object
    tag_AFTime = AFTime(timestamp)
    tag_AFValue = AFValue(tag_Value, tag_AFTime)
    tag_AFValue.Value = value
    tag = PIPoint.FindPIPoint(piServer, tagname)
    tag_UpdateOption = AFUpdateOption.Replace #options: (Replace,Insert,NoReplace,ReplaceOnly,InsertNoCompression,Remove)
    tag_BufferOption = AFBufferOption.DoNotBuffer #options: (DoNotBuffer,BufferIfPossible,Buffer)
    tag.UpdateValue(tag_AFValue, tag_UpdateOption, tag_BufferOption)
    return tag_AFValue




#create the import function to display all properties of an AFValue object
def Display_AFValue_Properties(AFValue):
    print(AFValue.AdditionalInfo)
    print(AFValue.Annotated)
    print(AFValue.Attribute)
    print(AFValue.CompareTo)
    print(AFValue.Convert)
    print(AFValue.Create)
    print(AFValue.CreateSystemNoDataFound)
    print(AFValue.CreateSystemStateValue)
    print(AFValue.DefaultValue)
    print(AFValue.Equals)
    print(AFValue.Finalize)
    print(AFValue.FromPIValue)
    print(AFValue.GetAnnotation)
    print(AFValue.GetHashCode)
    print(AFValue.GetType)
    print(AFValue.IsGood)
    print(AFValue.MemberwiseClone)
    print(AFValue.Overloads)
    print(AFValue.PIPoint)
    print(AFValue.Persist)
    print(AFValue.Questionable)
    print(AFValue.ReferenceEquals)
    print(AFValue.SetAnnotation)
    print(AFValue.Status)
    print(AFValue.Substituted)
    print(AFValue.Timestamp)
    print(AFValue.ToPIValue)
    print(AFValue.ToString)
    print(AFValue.UOM)
    print(AFValue.Value)
    print(AFValue.ValueAsDouble)
    print(AFValue.ValueAsInt32)
    print(AFValue.ValueAsSingle)
    print(AFValue.ValueType)
    print(AFValue.ValueTypeCode)