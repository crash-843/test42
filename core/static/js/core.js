$(function(){
  $("#edit_contact_form").ajaxForm({

    beforeSend: function(){
      $(':input').attr("disabled", true);
      $('.text-error').html('');
      $('#edit_contact_error').css("display", "none");
      $('#edit_contact_successful').css("display", "none");
      $('#edit_contact_progress_bar .bar').width("0%");
      $('#edit_contact_successful').css("display", "none");
      $('#edit_contact_progress_bar').css("display", "block");
    },
    
    success : function(responce) {
      $(':input').attr("disabled", false);
      $('#edit_contact_progress_bar').css("display", "none");
      data = $.parseJSON(responce)
      is_error = data['is_error']
      if (is_error) {
        errors = data['errors'];
        $.each(errors, function(key, val) {
          $('#'+key+' .text-error').append('<li>'+val+'</li>');
        });
        $('#edit_contact_error').css("display", "block");
      }else{
        $('#edit_contact_successful').css("display", "block");
        // alert(data['photo']);
        $('#user_photo').attr("src", data['photo']);
      };
    },
    
    uploadProgress: function(event, position, total, percentComplete){
      $('#edit_contact_progress_bar .bar').width(percentComplete+"%");
    }

  });
});
