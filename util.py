from html import escape

fmtr = get_ipython().display_formatter.formatters['text/html']

def getfmtr(obj, func=None):
    if fmtr.for_type(type(obj)):
        return fmtr.for_type(type(obj))(obj)
    else:
        return escape(obj.__str__()).replace("\n", "<br>")

def strfmtr(obj):
    return escape(obj.__str__()).replace("\n", "<br>")
fmtr.for_type(str, strfmtr)

def listfmtr(self):
    _repr_ = []
    _repr_.append("<table>")
    for item in self:
        _repr_.append("<tr>")
        _repr_.append("<td>")
        _repr_.append(getfmtr(item))
        _repr_.append("<td>")
        _repr_.append("</tr>")
    _repr_.append("</table>")
    return str().join(_repr_)
fmtr.for_type(list, listfmtr)

def tuplefmtr(self):
    _repr_ = []
    for item in self:
        _repr_.append("<td>")
        _repr_.append(getfmtr(item))
        _repr_.append("</td>")
    return str().join(_repr_)
fmtr.for_type(tuple, tuplefmtr)

fmtr.for_type(float, lambda x: f"{x:.0f}")