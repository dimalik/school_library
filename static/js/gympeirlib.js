$(document).ready(function() {
	
    $(".no-border td").css({
        'border-color': '#fff'
    })
    $("div#lib-footer .col-lg-12:first-child").addClass("lib-footer-wrap")
    $(".lib-footer-wrap .col-lg-4").addClass("lib-footer-column")
    $("#alerts").hide();
    /*$(".tab-pane table tr td:first-child").css({
        "background-color": "#f5f5f5",
        "width": "30%"
    });*/
    $('.close').click(function() {
        $('.alert').hide();
    })
    $("#print").click(function() {
        $.get("/bookshelf/make_pdf", {
            'book_id': book_id
        }).done(function(data) {
            window.open(data);
        });
    });
    $('#star').raty({
        starHalf: params['starHalf'],
        starOn: params['starOn'],
        starOff: params['starOff'],
        score: params['bookScore'],
        click: function(score, evt) {
            $.ajax({
                type: "POST",
                url: params['rate_url'],
                dataType: "json",
                data: {
                    'book': params['book_id'],
                    'score': score,
                    'csrfmiddlewaretoken': params['csrf_token']
                },
                success: function(response) {
                    $("#alerts").removeClass("alert-success alert-warning alert-danger").hide();

                    if (response.code == 403) {
                        $("#alerts").addClass("alert-danger");
                    } else {
                        $("#alerts").addClass("alert-success");
                    }

                    $("div#alerts").show()
                    $("div#alerts > p.alert-message").html(response.content)
                },
                error: function() {
                    $("#alerts").addClass("alert-danger");
                    $("#alerts").show()
                    $("div#alerts > p.alert-message").html("Υπήρξε κάποιο πρόβλημα στη σύνδεση. Προσπαθήστε ξανά αργότερα ή επικοινωνήστε με το διαχειριστή.");
                }
            });
        }
    });


    $("#reserve").click(function() {
        $.ajax({
            type: "POST",
            url: params['res_url'],
            dataType: "json",
            data: {
                'book': params['book_id'],
                'csrfmiddlewaretoken': params['csrf_token']
            },
            success: function(response) {
                $("#alerts").removeClass("alert-success alert-warning alert-danger").hide();
                if (response.code == 201) {
                    $("#alerts").addClass("alert-success");
                } else if (response.code == 500) {
                    $("#alerts").addClass("alert-warning");
                } else if (response.code == 404) {
                    $("#alerts").addClass("alert-danger");
                }
                $("div#alerts").show()
                $("div#alerts > p.alert-message").html(response.content)
            },
            error: function() {
                $("#alerts").addClass("alert-danger");
                $("#alerts").show()
                $("div#alerts > p.alert-message").html("Υπήρξε κάποιο πρόβλημα στη σύνδεση. Προσπαθήστε ξανά αργότερα ή επικοινωνήστε με το διαχειριστή.");
            }
        });
    });

    $(".list-add").click(function() {
        $.ajax({
            type: "POST",
            url: params['list_url'],
            dataType: "json",
            data: {
                'book': params['book_id'],
                'list': $(this).attr("data-list-id"),
                'csrfmiddlewaretoken': params['csrf_token']
            },
            success: function(response) {
                $("#alerts").removeClass("alert-success alert-warning alert-danger").hide();
                if (response.code == 201) {
                    $("#alerts").addClass("alert-success");
                } else if (response.code == 500) {
                    $("#alerts").addClass("alert-warning");
                }
                $("div#alerts").show()
                $("div#alerts > p.alert-message").html(response.content)
            },
            error: function() {
                $("#alerts").addClass("alert-danger");
                $("#alerts").show()
                $("div#alerts > p.alert-message").html("Υπήρξε κάποιο πρόβλημα στη σύνδεση. Προσπαθήστε ξανά αργότερα ή επικοινωνήστε με το διαχειριστή.");
            }
        });
    });


})
