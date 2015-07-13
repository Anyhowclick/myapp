/*function validateForm() {
    var user = document.getElementById('ajax').value;
    if(user === "Bangkok, Thailand (BKK-Suvarnabhumi Intl.)" || user === "Bangkok, Thailand (DMK-Don Mueang Intl.)" ){
        $(function() {
            alert("right");
        });
    }else{
        $(function() {
            alert("Wrong");
        });
    }
}*/
var submit = false;   

/*$.verify.addRules({
  dest: function(r) {
    if(r.val() == 'Bangkok, Thailand (BKK-Suvarnabhumi Intl.)' || r.val() == 'Bangkok, Thailand (DMK-Don Mueang Intl.)'){
        submit = true;
        return true;
    }else{
        submit = false;
        return "Not a valid destination";
    }
      //return "invalid";
    //return true;
  }
});*/

function validateForm() {
    
    var elem = document.getElementById("selection"),
    elem = elem.value;
    
    if(elem === ""){
        alert("empty");
    }else{
        submit = true;
    }
    
    if(submit){
        alert("submitted "+elem);
        return true;
    }
        alert("nono");
        return false;
    
}