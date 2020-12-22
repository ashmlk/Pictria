const imagePreviewContainer = `
<div class="m-1 border pt-3" style="min-height: 100px" id="image_create_preview">
  <div id="image_preview_icons_text">
    <div class="h4 mb-2 text-center text-darkt">
      Add an image to share...
    </div>
    <div class="my-2 text-center">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-images" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M12.002 4h-10a1 1 0 0 0-1 1v8l2.646-2.354a.5.5 0 0 1 .63-.062l2.66 1.773 3.71-3.71a.5.5 0 0 1 .577-.094l1.777 1.947V5a1 1 0 0 0-1-1zm-10-1a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-10zm4 4.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
        <path fill-rule="evenodd" d="M4 2h10a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1v1a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2h1a1 1 0 0 1 1-1z"/>
      </svg>
    </div>
  </div>
</div>
<div class="d-flex justify-content-center preview-box">
<div>
<button type="button" class="close btn btn-sm bg-secondary text-white border reset-image-preview" style="margin-left:7px;margin-bottom:-2px;display:none;border-radius:50%; padding-left:4px;padding-right:4px;" aria-label="Close">
<span aria-hidden="true">&times;</span>
</button>
<img src="" id="preview_image_image"/>
</div>
</div>
`

const isBookmarked = 
`
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark-fill" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5V2z"/>
</svg>
Bookmarked
`

const notBookmarked = 
`
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bookmark" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z"/>
</svg>
Bookmark
`

const successTick =
`
<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
  <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
  <path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
</svg>
`

const coverOverlay = 
`
<div class="collection-cover-overlay p-1" id="coverTagOverlay">
    <div class="small float-right">
        <div class="cover-tag btn btn-sm bg-light rounded-corners small text-dark" style="font-size:0.92rem;">
            Collection Cover
        </div>
    </div>
</div>
`

let actionButton = null;

$(document).ready(function () {

      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }

      var csrftoken = getCookie('csrftoken');

      function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

      $('.grid').imagesLoaded().progress(function() {
        $('.grid').masonry({
          itemSelector: '.grid-item',
          percentPosition: true,
          columnWidth: '.grid-sizer',
          isFitWidth: true,
        })
        $('.grid').masonry('reloadItems');
      })

      var infinite = new Waypoint.Infinite({
        element: $('.infinite-container')[0],
        onBeforePageLoad: function () {
          $('.loading').show();
        },

        onAfterPageLoad: function ($items) {
          $('.loading').hide();
          $('.grid').masonry('reloadItems');
          $('.grid').masonry('layout');
        }
      });

      $('#modal-image').on('hide.bs.modal', function (e) {
        $('.image-object').find('.image-overlay').removeClass('no-hover-effect');
      })

      $('#modal-image').on('show.bs.modal', function (e) {
        $('.image-object').find('.image-overlay').addClass('no-hover-effect');
      })

      $(document).on('click', '.btn-image-like', function(e) {
        e.preventDefault();
        let likeBtn = $(this);
        let formObj = $(likeBtn).closest('form');
        let like_url = $(formObj).attr('data-url');
        let form = $(formObj).serialize();
        $.ajax({
          url: like_url,
          type: 'POST',
          data: form,
          dataType:'json',
          success: function(data){
            $(formObj).closest('.image-likes').html(data.like);
          }
        })
      })
      $(document).on('click', '.image-object', function () {
        let image = $(this);
        let obj_url = $(image).attr('data-url');
        $.ajax({
          url: obj_url,
          type: 'GET',
          dataType:'json',
          beforeSend: function(){
            $('#modal-image').modal('show');
          },
          success: function(data){
            $('#modal-image .modal-content').html(data.image);
          }
        })
      })

      $(document).on('click', '.create-collection-btn', function () {
        let image = $(this);
        let obj_url = $(image).attr('data-url');
        $.ajax({
          url: obj_url,
          type: 'GET',
          dataType:'json',
          beforeSend: function(){
            $('#modal-image').modal('show');
          },
          success: function(data){
            $('#modal-image .modal-content').html(data.html_form);
          }
        })
      })

      $(document).on('click', '.create-image-btn', function () {
        let image = $(this);
        let obj_url = $(image).attr('data-url');
        $.ajax({
          url: obj_url,
          type: 'GET',
          dataType:'json',
          beforeSend: function(){
            $('#modal-image').modal('show');
          },
          success: function(data){
            $('#modal-image .modal-content').html(data.html_form);
            $('#div_id_image_photo').append($(imagePreviewContainer));
          }
        })
      })

      $(document).on('click', '#image_create_preview', function () {
        $('#id_image_photo').click();
      })      

      function readURL(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            $('#preview_image_image').attr('src', e.target.result);
          }
          
          reader.readAsDataURL(input.files[0]); // convert to base64 string
        }
      }
      
      $(document).on('change',"#id_image_photo", function() {
        $('#div_id_image_photo').find('#image_create_preview').remove();
        $('.preview-box').find('button').show();
        readURL(this);
      });

      $(document).on('click','.reset-image-preview', function() {
        $('.preview-box').remove();
        $('#preview_image_image').attr('src','');
        $('#id_image_photo').val('');
        $('#div_id_image_photo').append($(imagePreviewContainer));
      })

      $(document).on('submit','.image-create-form', function (e){
        e.preventDefault();     
        let formURL = $(this).attr("data-url");
        var form = new FormData(this);
        $.ajax({
          url: formURL,
          type: 'POST',
          data: form,
          cache: false,
			    processData: false,
			    contentType: false,
          dataType:'json',
          success: function(data){
            if($('#profile_latest__page__user').length){
              $('.image-count-info').html(`${data.img_count}<br>${data.img_text}`)
              $('#modal-image .modal-body').html($(successTick));
              $('#modal-image .modal-header .modal-title').html("<span>Posted Successfully</span>");
              setTimeout(function () {
                $('#modal-image').modal('hide');
              },2500);
              $(".profile__image__container").find(".grid").prepend(data.image_object).masonry("reloadItems");
              $(".grid").masonry("reloadItems");
              $(".grid").masonry("layout");
            }
            else {
              $('#modal-image .modal-body').html(successTick);
              $('#modal-image .modal-header .modal-title').html("<span>Posted Successfully</span>");
                setTimeout(function () {
                  $('#modal-image').modal('hide');
                },2500);
            }
          }
        })
      })

      $(document).on('click', '#searchbar_n', function () {
        $('.search-query-results').show();
      })

      $(document).on('click', function (e) {
        e.stopImmediatePropagation();
        $('.search-query-results').hide();
      });

      $(document).on('click', '.image-object-dropdown-button', function(){
        let bookmarkButton = $(this).closest('.dropdown').find('.image-drop-down-actions').find('.bookmark-image-button');
        let bookmarkUrl  = $(bookmarkButton).attr("data-url");
        $.ajax({
          url: bookmarkUrl,
          type: 'GET',
          dataType:'json',
          success: function(data){
            if(data.is_bookmarked){
              $(bookmarkButton).html(isBookmarked);
            } else if (!data.is_bookmarked) {
              $(bookmarkButton).html(notBookmarked);
            }
          }
        })
      })

      $(document).on('click', '.bookmark-image-button', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        let bookmarkButton = $(this);
        let bookmarkUrl = $(bookmarkButton).attr("data-url");
        $.ajax({
          url: bookmarkUrl,
          type: 'POST',
          dataType:'json',
          data: {
            csrfmiddlewaretoken: getCookie('csrftoken')
          },
          success: function(data){
            if(data.is_bookmarked){
              console.log('bookmarked')
              $(bookmarkButton).html(isBookmarked);
            } else if (!data.is_bookmarked) {
              $(bookmarkButton).html(notBookmarked);
            }
          }
        })
      })

      $(document).on('click', '.action-image-button', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#model-image').modal('hide');
        let actionUrl = $(this).attr("data-url");
        $.ajax({
          url: actionUrl,
          type: 'GET',
          dataType:'json',
          beforeSend: function(){
            $('#modal-image').modal('show');
          },
          success: function(data){
            $('#modal-image .modal-content').html(data.html_form);
          }
        })
      })

      $(document).on('submit', '.action-image-form', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        let imageIdentifier = $(this).attr("data-img-sc");
        let actionUrl = $(this).attr("data-url");
        let form = $(this).serialize();
        $.ajax({
          url: actionUrl,
          type: 'POST',
          dataType:'json',
          data:form,
          success: function(data){
            if(data.image_deleted_successfully) {
              $(`#img_ctr__${imageIdentifier}`).remove();
              $('.grid').masonry('reloadItems');
              $('.grid').masonry('layout');
              $('#modal-image .modal-body').html("<div class='my-2'>Your image has been removed successfully</div>");
              $('#modal-image .modal-header .modal-title').html("<span>Image Removed</span>");
              $('#modal-image .modal-footer').empty();
              setTimeout(function () {
                $('#modal-image').modal('hide');
              },1100);
              if($('#profile_latest__page__user').length){
                $('.image-count-info').html(`${data['img_count']}<br>${data['img_text']}`)
              } else if($('#profile_collections__page__user').length){
                $('.image-collections-count-info').html(`${data['collection_count']}<br>Collections`)
              }
            } else if (data.edited_successfully) {
              $(`#img_ctr__${imageIdentifier}`).find('.image-description').find('.image__description__text').html(data.new_description);
              $(`#img_ctr__${imageIdentifier}`).find('.image-tags').empty();
              let tagsContainer = $(`#img_ctr__${imageIdentifier}`).find('.image-tags');
              for (tag in data.tags){
                let tagName = data.tags[tag]['name'].replace(/\s/g, '');
                let a =  `<a class="text-dark mr-1" href="/tags/${data.tags[tag]['slug']}/">#${tagName}</a>`
                $(tagsContainer).prepend(a);
              }
              $('#modal-image .modal-body').html($(successTick));
              $('#modal-image .modal-header .modal-title').html("<span>Image Updated</span>");
              setTimeout(function () {
                $('#modal-image').modal('hide');
              },2500);
            }
          }
        })
      })

      var search_url = "/search?q="
      $(document).on('keyup','#searchbar_n', function () {
        if($(this).val()){
          var q = $(this).val();
          $.ajax({
            type: "GET",
            url: "/search?q=" + q,
            dataType: 'json',
            success: function (data){
              if(data.profiles.length > 0){
                $('#user_results').find('li').remove();
                for (p in data.profiles){
                  let user = createUser(q, data.profiles[p]['username'],data.profiles[p]['first_name'],data.profiles[p]['last_name'])
                  $('#user_results').append(user);
                }
              }
              if(data.terms.length > 0){
                $('#term_results').find('li').remove();
                for (p in data.terms){
                  let term = createTerm(q, data.profiles[p]['text'])
                  $('#term_results').append(user);
                }
              }
              
              $('.search-query-results').show()
            },
            error: function(rs, e){
                console.log(rs.responeText);
            },
        })
        } else {
          $('.search-query-results').hide()
        }
      });

      function createUser(q, username, firstName, lastName){
        let a = document.createElement('a');
        a.setAttribute('href', `/results?q=${q}`)
        let li = document.createElement('li');
        li.className = "list-group-item text-dark search-link"
        let content = 
        `
        <div class="h6">
          ${firstName} ${lastName}
        </div>
        <div class="small">
          ${username}
        </div>
        `
        li.innerHTML = content;
        a.appendChild(li);
        return a;
      }

      function createTerm(q, text){
        let a = document.createElement('a');
        a.setAttribute('href', `/results?q=${q}`)
        let li = document.createElement('li');
        li.className = "list-group-item text-dark search-link"
        let content = 
        `
        <div class="h6">
          ${term}
        </div>
        `
        li.innerHTML = content;
        a.appendChild(li)
        return a;
      }
      Dropzone.autoDiscover = false;
      $('#modal-image').on("shown.bs.modal", function () {
        if ($("#my-dropzone").length) {
            var myDropzone = new Dropzone("#my-dropzone" , {
            dictDefaultMessage: '',
            addRemoveLinks: true,
            acceptedFiles: ".jpeg,.jpg,.png",
            uploadMultiple: true,
            url: "/create/collection/",
            autoProcessQueue: false,
            paramName: "images",
            maxFiles: 10,
            thumbnailWidth: 230,
            dictRemoveFile : 'Remove',
            thumbnailHeight: 250,
            parallelUploads: 10,
            previewTemplate: document.getElementById('preview-template').innerHTML,
            previewsContainer: "#preview-selected",

            init: function () {
                var myDropzone = this;
                $('.collection-post-submit-button').on("click", function (e) {
                    if (myDropzone.getQueuedFiles().length > 0) { 	
                        e.preventDefault();
                        e.stopImmediatePropagation();
                        myDropzone.processQueue();
                    } else {                     
                        myDropzone.uploadFiles([]); //send empty 
                    }                                    
                });

                this.on("addedfiles", function () {
                    let parentImage = $('#preview-selected').children().first();
                    $(parentImage).append(coverOverlay);
                    $("#collectionCoverIndex").val("0");
                    $("#add-images").css("height","100%");
                })

                this.on("maxfilesexceeded", function() {
                    if (this.files[1]!=null){
                      this.removeFile(this.files[0]);
                    }
                });

                this.on('sendingmultiple', function(files, xhr, formData) {
                var data = $('.collection-create-form').serializeArray();
                $.each(data, function(key, el) {
                    formData.append(el.name, el.value);
                    });
                });

                this.on("successmultiple", function (files, data) {
                    if(data.collection_created){
                        if($('#profile_collections__page__user').length){
                            $(".grid").prepend(data.collection_object).masonry("reload");; 
                            $(".grid").masonry("reloadItems");
                            $(".grid").masonry("layout");
                            $('.image-collections-count-info').html(`${data['collection_count']}<br>Collections`)
                        }
                        $('#modal-image .modal-body').html($(successTick));
                        $('#modal-image .modal-header .modal-title').html("<span>Collection Created</span>");
                        setTimeout(function () {
                        $('#modal-image').modal('hide');
                        },2500);
                        
                    } else {
                        $('#modal-image .modal-content').html(data.html_form)
                    }
                });

                this.on("error", function (files, data) {
                });

                this.on("completemultiple", function(file) {
                    myDropzone.removeFile(file);
                });
            }
            });
          }
      })
      

      $(document).on("click",'.dz-image-preview', function () {
          $("#coverTagOverlay").remove();
          $(this).append(coverOverlay);
          $("#collectionCoverIndex").val($(this).index())
      })
      
      $(document).on("click",'#add-images', function () {
          $('#my-dropzone').get(0).dropzone.hiddenFileInput.click();
      })
})