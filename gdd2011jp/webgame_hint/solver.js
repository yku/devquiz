var cards = document.getElementsByTagName("td").length;
a = new Array;
var myevent = document.createEvent('MouseEvents');
myevent.initEvent('click', false, true);

// カード全部の色取得
for(var i = 0; i < cards; i++) {
    var element = document.getElementById('card'+i);
    
    if (element == null) {
        alert('Card element is not found. Check element id.');
    } else {
        element.dispatchEvent(myevent);
        a.push({color:element.style.backgroundColor, id:i});
        //alert('Card color is "' + element.style.backgroundColor + '".');
    }
}

for(var i = 0; i < cards; i++) {
    if(a[i]["id"] == -1) continue;

    var one = a[i]["color"];
    for(var j = i+1; j < cards; j++) {
        var two = a[j]["color"];
        if(a[j]["id"] == -1 || one != two) continue;
        // 終わったやつはidを-1にしとく
        a[i]["id"] = -1;
        a[j]["id"] = -1;
        
        var element = document.getElementById('card'+i);
        element.dispatchEvent(myevent);
        element = document.getElementById('card'+j);
        element.dispatchEvent(myevent);
    }
}
