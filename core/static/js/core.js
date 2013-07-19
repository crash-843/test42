$(function(){
  $("#edit_contact_form").ajaxForm({

    beforeSend: function(){
      $(':input').attr("disabled", true);
      $('.text-error').html('');
      $('.alert-success').hide();
      $('.alert-error').hide();
      $('.edit_contact_progress .bar').width("0%");
      $('.edit_contact_progress').show();
    },
    
    success : function(response) {
      $(':input').attr("disabled", false);
      $('.edit_contact_progress').hide();
      data = $.parseJSON(response)
      is_error = data['is_error']
      if (is_error) {
        errors = data['errors'];
        $.each(errors, function(key, val) {
          $('#'+key+' .text-error').append('<li>'+val+'</li>');
        });
        $('.alert-error').show();
      }else{
        $('.alert-success').show();
        $('#photo img').attr("src", data['photo']);
        $('#id_photo').val('')
      };
    },
    
    uploadProgress: function(event, position, total, percentComplete){
      $('.edit_contact_progress .bar').width(percentComplete+"%");
    }

  });
});
