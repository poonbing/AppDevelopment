var classic = document.querySelectorAll(".Classic")
var luxury = document.querySelectorAll(".Luxury")
var cardistry = document.getElementsByClassName(".Cardistry")
var all = document.querySelectorAll(".Classic,.Luxury,.Cardistry")
function FilterClassic(type) {
    for (i; i < all.length; i++) {
        all.style.display = 'none';
    });
    for (i; i < classic.length; i++) {
        classic.style.display = 'flex';
    });
}
function FilterLuxury(type) {
    for (i; i < all.length; i++) {
        all.style.display = 'none';
    });
    for (i; i < all.luxury; i++) {
        luxury.style.display = 'flex';
    });
}
function FilterCardistry(type) {
    for (i; i < all.length; i++) {
        all.style.display = 'none';
    });
    for (i; i < cardistry.length; i++) {
        cardistry.style.display = 'flex';
    });
};


function FilterLuxury(type) {
    for (i; i < all.length; i++) {
        all.style.display = 'none';
    };
    for (i; i < all.luxury; i++) {
        luxury.style.display = 'block';
    };
}
function FilterCardistry(type) {
    for (i; i < all.length; i++) {
        console.log(all.length)
        console.log('your mom')
        all.style.display = 'block';
    };
    for (i; i < cardistry.length; i++) {
        cardistry.style.display = 'block';
    };
};

function Filter(type) {
    if (type == "classic"){
        var cum = classic;
    } else if (type == "luxury"){
        var cum = luxury;
    } else if (type == "cardistry"{
        var cum = cardistry;
    };
    for (i; i < classic.length; i++) {
        console.log("gay")
        cum[i].style.display = 'block';
    };
}
