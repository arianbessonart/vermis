$(function() {

    // $( "#date_created_id" ).datepicker();
    // $( "#date_created_id" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
    // $( "#date_created_id" ).datepicker( "option", "dateFormat", "dd/mm/yy" );
});

$('body').on('keyup','.price', function (event) {
	event.preventDefault();
  calculate_total();
});

function calculate_total () {
  var sub_total = 0;
  $('.price').each(function() {
        sub_total += Number($(this).val());
    });
    sub_total = sub_total.toFixed(2);
    $('#id_sub_total').val(sub_total);
    var iva = sub_total*0.22;
    iva = iva.toFixed(2);
    $('#id_iva').val(iva);
    var total = Number(iva) + Number(sub_total);
    total = total.toFixed(2);
    $('#id_total').val(total);

}

var newRowContent = '<tr><td><input type="text" value="" class="form-control" placeholder="Detalle" name="input_description" /></td><td><input type="text" placeholder="Precio" class="form-control price" name="input_price" /></td><td><a href="#" class="glyphicon glyphicon-minus delete-item-table"></a></td></tr>';
$('.add-item-table').click(function () {
  $("#item-table tbody").append(newRowContent);
})

$('body').on('click','.delete-item-table',function () {
  var tr = $(this).closest('tr');
  tr.remove();
  calculate_total();
})



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$('#input_client').change(function(){
  load_client_data();
});

function load_client_data () {
  var val = $('#input_client').val();
  rut_value = "-";
  address_value = "-";
  if (val != ""){
    rut_value = rut_dict[val];
    address_value = address_dict[val];
  }
  $('#rut_label').text(rut_value);
  $('#address_label').text(address_value);
}


$(document).ready(function() {

  $('body').on('click','#yes',function () {
    $("#date-charged-div").removeClass('hide');
  });

  $('body').on('click','#no',function () {
    $("#date-charged-div").addClass('hide');
  });

  $('#date-charged-form').on('submit', function(event){
    event.preventDefault();
    var charged_invoice = $('input[name=optionsCharge]:checked').attr('id') == 'yes' ? true : false;
    var data = { charged: charged_invoice,date_charged : $('#id_date_charged').val()};
    $.ajax({
        url : "set_charged_invoice/", // the endpoint
        type : "POST", // http method
        data : data, // data sent with the post request
        traditional: true,
        // handle a successful response
        success : function(json) {
            $('.modal').modal('hide');
            // location.reload(true);
            window.location.href=window.location.href
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            // $('#message_modal').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
  });

  $('#filter').keyup(function () {
    var rex = new RegExp($(this).val(), 'i');
    $('.searchable tr').hide();
    $('.searchable tr').filter(function () {
        return rex.test($(this).text());
    }).show();

  });

  $('.searchable > tr').click(function() {
    var href = $(this).attr("href");
    if(href) {
        window.location = href;
    }
  });


  $('#datetimepicker5').datetimepicker({
          pickTime: false
  });

  $('#register-form').find('[name="input_client"]')
    .selectpicker()
    .change(function(e) {
        // revalidate the language when it is changed
        $('#register-form').bootstrapValidator('revalidateField', 'input_client');
    }).end();

  $('#register-form').bootstrapValidator({
      excluded: ':disabled',
      feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
      },
      fields: {
          input_name: {
            validators: {
              notEmpty: {
                  message: 'El nombre es requerido y no puede ser vacío'
              },
            }
          },
          input_rut: {
            validators: {
              notEmpty: {
                message: 'El RUT es requerido y no puede ser vacío'
              },
              stringLength: {
                min: 12,
                max: 12,
                message: 'El RUT debe tener 12 números'
              },
              regexp: {
                regexp: /^[0-9]+$/,
                message: 'El RUT debe contener únicamente números'
              },
            }
          },
          input_address: {
            validators: {
                notEmpty: {
                    message: 'La dirección es requerida y no puede ser vacía'
                },
            }
          },
          // input_date_created: {
          //   validators: {
          //     notEmpty: {
          //         message: 'Debe seleccionar una fecha'
          //     },
          //     date: {
          //         format: 'DD/MM/YYYY',
          //         message: 'No es una fecha válida'
          //     }
          //   }
          // },
          input_client: {
              validators: {
                notEmpty: {
                    message: 'Debe seleccionar un cliente'
                }
              }
          },
          input_reference: {
            validators: {
              regexp: {
                regexp: /^[0-9]+$/,
                message: 'Únicamente números permitidos'
              }
            }
          }
      }
  });

  $('#date-charged-form').bootstrapValidator({
      excluded: ':disabled',
      feedbackIcons: {
          valid: 'glyphicon glyphicon-ok',
          invalid: 'glyphicon glyphicon-remove',
          validating: 'glyphicon glyphicon-refresh'
      },
      fields: {
          // input_date_charged: {
          //   validators: {
          //     notEmpty: {
          //         message: 'Debe seleccionar una fecha'
          //     }
          //   }
          // },
      }
  });
});

