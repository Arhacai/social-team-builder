$( document ).ready(function() {

  $('textarea').autogrow({onInitialize: true});


  //Cloner for infinite input lists for skills
  $(".circle--clone--list").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
    var total = $("#id_form-TOTAL_FORMS").val();
    var name = 'form-' + total + '-skill';
    copy.find("input").attr({"name": name, "id": "id_" + name}).val('');
    $("#id_form-TOTAL_FORMS").val(parseInt(total)+1);
  });

  $(".circle--clone--list").on("click", "li:not(:nth-child(5)) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    parent.remove();
    var total = $("#id_form-TOTAL_FORMS").val();
    $("#id_form-TOTAL_FORMS").val(parseInt(total)-1);
  });

  //Cloner for infinite input lists for positions
  $(".circle--clone--list--position").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
    var total = $("#id_form-TOTAL_FORMS").val();
    var title = 'form-' + total + '-title';
    var description = 'form-' + total + '-description';
    copy.find("input").attr({"name": title, "id": "id_" + title}).val('');
    copy.find("textarea").attr({"name": description, "id": "id_" + description}).val('');
    $("#id_form-TOTAL_FORMS").val(parseInt(total)+1);
  });

  $(".circle--clone--list--position").on("click", "li:not(:nth-child(5)) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    parent.remove();
    var total = $("#id_form-TOTAL_FORMS").val();
    $("#id_form-TOTAL_FORMS").val(parseInt(total)-1);
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });




});