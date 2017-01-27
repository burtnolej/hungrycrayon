// define module alertmeshirtcolor as a function that depends on shirt.js 
define(["app/shirt"], function(shirt) {
        return function(msg)  {
                  alert(shirt.color);
        }
    }
);
