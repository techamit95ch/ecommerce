$(document).ready( function () {
    // Contact formData
     var contactForm = $('.contact-form');

     contactForm.submit(function(event){
         event.preventDefault();
         var contactFormMethod = contactForm.attr('method');
         var contactFormAction = contactForm.attr('action');
         var contactFormSubmitBtn = contactForm.find("[type='submit']");
         var contactFormData = contactForm.serialize();
         var contactFormSubmitBtnText = contactFormSubmitBtn.text();
         $.ajax({
             url:contactFormAction,
             data:contactFormData,
             method:contactFormMethod,
             beforeSend:displaySubmitting(true),
             success: function(data) {
                 contactForm[0].reset();
                 $.alert({
                      title:"Success!",
                      content: data.message,
                      theme: "modern",

                  });
                  displaySubmitting(false);

             },
             error: function(err){
                 console.log(err);
                 var jsonData = err.responseJSON;
                 var msg ="";
                 $.each(jsonData,function(key,value){
                     msg +=key+" :  "+ value[0].message + "<br/>";
                 });
                 $.alert({
                     title:"Oops!",
                     content: msg,
                     theme: "supervan",
                 });
                 displaySubmitting(false);
             }
         });
         function  displaySubmitting(doSubmit){
             if (doSubmit){
                 contactFormSubmitBtn.addClass("disabled");
                 contactFormSubmitBtn.html("<i class='fa fa-spin fa-spinner'></i>");
             }else{
                 contactFormSubmitBtn.addClass("enabled");
                 contactFormSubmitBtn.html(contactFormSubmitBtnText);

             }
         }
     });
    // Serach Form Details
    var searchForm = $('.form-search');
    var searchInput = searchForm.find("[name='q']");
    var searchBtn =searchForm.find("[type='submit']");
    var typingTimer;
    var typingInterval = 1000;        // .5 sec
    searchInput.keyup(function(event){
      clearTimeout(typingTimer);
      typingTimer = setTimeout(performSearch,typingInterval);
    });
    searchInput.keydown(function(event){
      clearTimeout(typingTimer);
    });
    function  doSearchLoader(){
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i>");
    }
    function performSearch(){
      doSearchLoader();
      var query =searchInput.val();
      window.location.href="/search/?q="+query;
    }

    // Product Form details
    // cart + product
    var productForm = $('.form-product-ajax');
    productForm.submit(function(event) {
        event.preventDefault();
        //alert('I wont let you submit');
        var thisForm = $(this)
        var dataEndPoint = thisForm.attr("data-endPoint");
        var httpMethod = thisForm.attr('method');
        var formData = thisForm.serialize();
        // Some Ajax Data Here
        //console.log(actionUrl);
        $.ajax({
            url: dataEndPoint,
            method: httpMethod,
            data: formData,
            success: function(data) {
                // console.log('success');
                // console.log(data);
                var submitSpan = thisForm.find('.submit-span');
                var navbarCartCount = $('.navbar-cart-count');
                if (data.added) submitSpan.html(
                    '<button type="submit" class="btn btn-link"> Remove </button>'
                );
                else{
                  submitSpan.html(
                      '<button type="submit" class="btn btn-success">Add to Cart</button>'
                  );

                }
                navbarCartCount.text(data._count);
                if (window.location.href.indexOf('cart')!= -1) refreshCart(data.api);
            },
            error: function(err) {
                $.alert({
                    title:"Oops!",
                    content: "An error occured",
                    theme : "supervan"
                });
                console.log(err);
            }
        });
        function  refreshCart(refreshCartUrl){
            var cartTable = $('.cart-table')
            var cartBody= cartTable.find('.cart-body');
            var cart_sub_total= cartBody.find('.cart_sub_total');
            var cart_total= cartBody.find('.cart_total');

            var refreshCartMethod = "GET";
            $.ajax({
                url: refreshCartUrl,
                data:{},
                method:refreshCartMethod,
                success: function(data){
                    // console.log(data);
                    cart_sub_total.text(data.sub_total);
                    cart_total.text('Checkout ('+ data.total +')/-');
                }, error: function(err){
                    // alert(err)
                    console.log(err);
                }
            });
        }
    });
});
