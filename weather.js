var xpath = require('xpath'),
    dom = require('xmldom').DOMParser,
    fs = require('fs');

var xml = fs.readFileSync('artukainen.xml', 'utf8').toString();
var root = new dom().parseFromString(xml)



function find_values(xpath_query, doc) {
    var query = xpath.evaluate(
        xpath_query,
        doc,
        xpath.createNSResolver(root),
        xpath.XPathResult.ANY_TYPE,
        null)

    var results = []
    var e = query.iterateNext()
    while (e) {
        results.push(e.nodeValue)
        e = query.iterateNext()
    }
    return results
}



var temp_times  = find_values("//wml2:MeasurementTimeseries[@gml:id='obs-obs-1-1-t2m']/.//wml2:time/text()", root)
var temp_values = find_values("//wml2:MeasurementTimeseries[@gml:id='obs-obs-1-1-t2m']/.//wml2:value/text()", root)
console.log(temp_times)
console.log(temp_values)

var humid_times  = find_values("//wml2:MeasurementTimeseries[@gml:id='obs-obs-1-1-rh']/.//wml2:time/text()", root)
var humid_values = find_values("//wml2:MeasurementTimeseries[@gml:id='obs-obs-1-1-rh']/.//wml2:value/text()", root)
console.log(humid_times)
console.log(humid_values)
