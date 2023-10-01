$("#commentform").submit(function (e) {
    e.preventDefault();
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (res) {
            console.log("Comment saved to db..");
            if (res.bool == true) {
                // Reload the page with no delay
                location.reload();
            }
        }
    });
});


//for checkbox filter

$(document).ready(function(){
    $(".filter-checkbox").on("click", function(){
        let filter_object = {}

        $(".filter-checkbox").each(function(index){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            console.log(filter_key,filter_value);

            filter_object[filter_key]=Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).
            map(function(element){
                return element.value
            });
        });
        console.log(filter_object);
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: "json",
            beforeSend: function(){
                console.log("Sending data");
                this_value.hide()
            },
            success:function(response){
                this_value.show()
                console.log(response);
                console.log("Suceessfull");
                $("#filtered-products").html(response.data)
            }
        });
    });
});

//price range slider
$(document).ready(function() {
    // Function to update the filter object based on user input
    function updateFilterObject() {
        let min_price = $("#min_price").val();
        let max_price = $("#max_price").val();

        let filter_object = {
            min_price: min_price,
            max_price: max_price
        };

        // Additional code for handling checkbox filters (if needed)

        return filter_object;
    }

    // Function to handle the filter action
    function applyFilter() {
        let filter_object = updateFilterObject();

        // Perform your AJAX request with filter_object
        $.ajax({
            url: "/filter-products",
            data: filter_object,
            dataType: "json",
            beforeSend: function() {
                console.log("Sending data");
            },
            success: function(response) {
                console.log(response);
                console.log("Successful");
                $("#filtered-products").html(response.data);
            }
        });
    }

    // Event listeners for input elements and filter button
    $("#min_price, #max_price").on("input", function() {
        let min_price = $("#min_price").val();
        let max_price = $("#max_price").val();

        // Ensure min_price is less than or equal to max_price
        if (parseFloat(min_price) > parseFloat(max_price)) {
            $("#min_price").val(max_price);
        }

        // Update the range sliders
        $("#range1").val(min_price);
        $("#range2").val(max_price);

        // Apply the filter
        applyFilter();
    });

    $("#range1, #range2").on("input", function() {
        let min_price = $("#range1").val();
        let max_price = $("#range2").val();

        // Ensure max_price is greater than or equal to min_price
        if (parseFloat(max_price) < parseFloat(min_price)) {
            $("#range2").val(min_price);
        }

        // Update the number inputs
        $("#min_price").val(min_price);
        $("#max_price").val(max_price);

        // Apply the filter
        applyFilter();
    });

    // Event listener for the filter button
    // $("#filter-btn").on("click", function() {
    //     applyFilter();
    // });
});


//Add to cart

$(".add-to-cart-button").on("click", function(){
    let this_value = $(this)
    let index = this_value.attr("data-index")
    let product_id = $(".product-id-"+index).val()
    let quantity = $(".product-qty-"+index).val()
    let product_title = $(".product-title-"+index).val()
    let product_price = $(".product-price-"+index).text()
    let product_image = $(".product-image-"+index).val()
    console.log(product_price);
    $.ajax({
        url:'/add-to-cart',
        data:{
            'id': product_id,
            'qty': quantity,
            'title': product_title,
            'price': product_price,
            'image': product_image,
        },
        dataType: 'json',
        beforeSend:function(){
            console.log("Adding to the Cart");
        },
        success:function(response){
            this_value.html("Added")
            console.log("Item added ")
            $(".cart-item-count").text(response.totalcartitems)
        }
    })
});

// Delete the cart item


$(".delete-product").on("click", function(){
    let this_value = $(this);
    let product_id = $(this).data("product")
    console.log("hai")
    console.log(product_id);

    $.ajax({
        url: '/delete-product-from-cart',
        data: {
            'id': product_id,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Deleting")
        },
        success:function(response){
            $(".cart-item-count").text(response.totalcartitems)
            $("#cart-products").html(response.data)
            location.reload();
        }
    });
});
