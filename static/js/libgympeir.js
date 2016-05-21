$(document).ready(function() {
    var book_id = {{ vivlio.id }};
    var list_id = $(this).attr("data-list-id");
    
    function make_alerts_success(response) {
        $("#alerts").removeClass("alert-success alert-warning alert-danger").hide();
        if (response.code == 403) {
          $("#alerts").addClass("alert-danger");                    
        }
        else {
          $("#alerts").addClass("alert-success");                    
        }
        $("div#alerts").show()
        $("div#alerts > p.alert-message").html(response.content)
      }
      
      function make_alerts_error() {
          $("#alerts").addClass("alert-danger");
          $("#alerts").show()
          $("div#alerts > p.alert-message").html("Υπήρξε κάποιο πρόβλημα στη σύνδεση. Προσπαθήστε ξανά αργότερα ή επικοινωνήστε με το διαχειριστή.");
      }

    
  $('#star').raty({
    starHalf      : '{{ STATIC_URL }}img/star-half.png',
    score         : {{ vivlio.rating.get_rating|stringformat:'f' }},
    starOn        : '{{ STATIC_URL }}img/star-on.png',
    starOff       : '{{ STATIC_URL }}img/star-off.png',
    click         : function(score, evt) {
      $.ajax({
        type      : "POST",
        url       : "{% url "bookshelf_book_rate_view" %}",
        dataType  : "json",
        data      : {
          'book'  : {{ vivlio.id }},
          'score' : score,
          'csrfmiddlewaretoken' : '{{ csrf_token }}'
        },
        success : function(response) {
            make_alerts_success(response)
        }
         
        error : function() {
            make_alerts_error()
            }
        }); 
      }
     });

    $("#reserve").click(function() {
        $.ajax({
            type : "POST",
            url : "{% url "reservations_create_reservation" %}",
            dataType: "json",
            data : {
                'book' : book_id,
                'csrfmiddlewaretoken' : '{{ csrf_token }}'
                },
                success : function(response) {
                    make_alerts_success(response);
                    },
                error : function() {
                    make_alerts_error()
                    }
        });
    });


        $("#make_pdf").click(function() {
            $.ajax({
                type : "GET",
                url : "{% url "bookshelf_pdf_view" %}",
                dataType: "json",
                data : {
                    'book_id' : book_id,
                    'csrfmiddlewaretoken' : '{{ csrf_token }}'
                    },
                    error : function() {
                        make_alerts_error();
                        }
            });
        });

  $('.close').click(function() {

     $('.alert').hide();

  })
  
  
    $(".list-add").click(function() {


        $.ajax({
            type : "POST",
            url : "{% url "lists_add_book" %}",
            dataType: "json",
            data : {
                'book' : book_id,
                'list' : list_id,
                'csrfmiddlewaretoken' : '{{ csrf_token }}'
                },
                success : function(response) {
                    make_alerts_success(response);
                    },
                error : function() {
                    make_alerts_error();
                    }
        });
    });

  $("#alerts").hide()

