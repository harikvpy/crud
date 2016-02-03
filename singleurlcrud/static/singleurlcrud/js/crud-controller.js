/* crud-controller.js */
// variable will be set to true for popups from html
var _popup = false; 
/* 
   Returns the base url, including any paging arguments, while
   omitting the op and item arguments
 */
function get_opless_url() {
    var url = document.URL;
    var urlComponents = url.split('?');
    var base_url = urlComponents[0];
    var args = [];
    if (urlComponents.length > 1) {
        args = urlComponents[1].split('&');
    }
    var preservedArgs = [];
    for (var i=0; i<args.length; i++) {
        arg = args[i];
        var name = arg.split('=')[0];
        var value = '';
        if (name != 'o' && name != 'item' && name != 'items') {
            preservedArgs.push(arg);
        }
    }
    var isFirst = true;
    for (var i=0; i<preservedArgs.length; i++) {
        arg = preservedArgs[i];
        if (isFirst) {
            base_url += '?';
            isFirst = false;
        } else {
            base_url += '&';
        }
        base_url += arg;
    }
    return base_url;
}
/**
  Given a bunch of GET arguments (NVP), returns a URL consisting of
  arguments excluding the 'o' and 'item' arguments.
 */
function compose_url() {
    var url = get_opless_url();
    var isFirst= false;
    if (url.charAt(url.length-1) == '/') {
        isFirst = true;
    }
    for (var i=0; i<arguments.length; i++) {
        if (isFirst) {
            url += '?';
            isFirst = false;
        } else {
            url += '&';
        }
        url += arguments[i];
    }
    return url;
}
/* returns true if we're currently in CRUD 'edit' mode */
function inEditMode () {
    var url = document.URL;
    var components = url.split('?');
    if (components.length > 1) {
        var args = components[1].split('&');
        for (var i=0; i<args.length; i++) {
            var arg = args[i];
            var name = arg.split('=')[0];
            var value = "";
            if (arg.split('=').length > 1) {
                value = arg.split('=')[1];
            }
            if (name == 'o' && value == 'edit') {
                return true;
            }
        }
    }
    return false;
}
/* We use the global to pass information between functions. Crude, but it works! */
var item_to_delete = null; /* global stores the item to delete */
var delete_msg = ''; /* the message to be shown in delete confirmation panel */
var cSelectedItems = 0;
/* It's important that we have a django object in global namespace.
 * Functions in RelatedObjectLookup.js file from contrib.admin that 
 * we'll be including for the popup edit/add feature refer to 
 * jQuery from this object. This namespace will be created if 
 * admin:js18n url is included in the base template and if that 
 * url is accessible without user login. If the django object
 * is not present, we create an empty django object and assign
 * its jQuery property to the global jQuery object.
 *
 * Of course the contrib.admin django namespace has lot more
 * methods (specifically localized datetime formats and string
 * i18n methods), but for our CRUD, we don't need them.
 */
    if (typeof(django) == "undefined") {
        django = {};
    }
    if (typeof(django.jQuery) == "undefined" &&
            typeof(window.jQuery) == "function") {
        django.jQuery = window.jQuery;
    }
/* 
   Function to test the state whereby a previous add operation 
   resulted in an error. We can test this by checking for the the
   hidden input field 'id_form_haserrors' which will be set to 1
   if there were form validation errors. Also, if the view added
   its own errors, they would be displayed as alert messages, 
   presence of which can also indicates an error condition.

*/
function addErrorMode() {
    return  ($("#id_form_haserrors").length > 0 && $("#id_form_haserrors").val() == "1") ||
                $("#formEdit").children("div.alert").length > 0;
}
/* hides/shows the relevant sections based on document's CRUD mode */
$(document).ready(function() {
    doPostLoad();
});
function doPostLoad() {
    /* in Edit mode or in Add-error mode, we need to display
       the item edit panel and not the list of items.
     */
    if (inEditMode() || addErrorMode()) {
        $("#itemList").addClass('not');
        $("#editItemPanel").removeClass('not');
    } else {
        $("#editItemPanel").addClass('not');
        $("#itemList").removeClass('not');
    }
    delete_msg_templ = $("#msgDeleteConfirm").text();
    //$("#id_action_dropdown").hide();
    $("#id_select_all").click(function(evt) {
        if ($(evt.target).prop("checked"))
            selectAll();
        else
            selectNone();
    });
    hideActionMenu();
    $(".item-selection-checkbox").click(function(evt) {
        var cSelectedItemsPrev = cSelectedItems;
        if ($(evt.target).prop("checked"))
            cSelectedItems++;
        else
            cSelectedItems--;
        if (cSelectedItems > 0) {
            if (cSelectedItemsPrev == 0)
                showActionMenu();
            if (cSelectedItems == totalItems)
                $("#id_select_all").prop("checked", true);
            else
                $("#id_select_all").prop("checked", false);
        }
        else if (cSelectedItems == 0 && cSelectedItemsPrev > 0) {
            hideActionMenu();
            $("#id_select_all").prop("checked", false);
        }
    });
    // bind on change handler with related-object lookup select boxes
    $("[data-crfww]").change(function() {
        updateChangeRelatedLink($(this));
    });
    $(".change-existing").click(function() {
        event.preventDefault();
        if ($(this).attr('href'))
            return showRelatedObjectPopup(this);
    });
    $("[data-crfww]").each(function(index, element) {
        updateChangeRelatedLink($(element));
    });
}
function updateChangeRelatedLink(sel) {
    var selected = sel.val();
    var anchor = sel.parent().find(".change-existing");
    if (selected) {
        var templ = anchor.data().hreftempl;
        anchor.attr("href", templ.replace("__fk__", selected));
        anchor.removeClass("change-existing-disabled");
    } else {
        sel.parent().find(".change-existing").removeAttr("href");
        anchor.removeAttr("href");
        anchor.addClass("change-existing-disabled");
    }
}
function selectAll() {
    for (var i=0; i<totalItems; i++) {
        $("#id_select_"+i).prop("checked", true);
    }
    if (cSelectedItems == 0)
        showActionMenu();
    cSelectedItems = totalItems; 
}
function selectNone() {
    for (var i=0; i<totalItems; i++) {
        $("#id_select_"+i).prop("checked", false);
    }
    if (cSelectedItems > 0)
        hideActionMenu();
    cSelectedItems = 0;
}
function showActionMenu() {
    $("#id_action_dropdown").children("button").removeClass('disabled'); //fadeIn(400);
}
function hideActionMenu() {
    $("#id_action_dropdown").children("button").addClass('disabled'); //fadeOut(400);
}
/* Add new item button handler. Hide item list and show edit item section. */
function addNewItem() {
    window.location = compose_url("o=add")
}
/* edit an item */
function editItem(id) {
    window.location = compose_url("o=edit", "item="+id);
}
function deleteItem(id, name) {
    window.location = compose_url("o=delete", "item="+id);
}
/* 
   Cancel an ongoing edit operation. Depending on Edit/Add mode, take appropriate action.
   For the former mode, redirect to the base URL. In the case of hte latter mode,
   simply hide the edit panel and display the list of items
 */
function cancelEdit() {
    if (_popup) {
        // just dismiss the window
        window.close();
    } else {
        window.location = get_opless_url();
    }
}
/* hide the delete confirmation panel and display the item list */
function cancelDelete() {
    window.location = get_opless_url();
}
/* action to delete multiple items */
function deleteMultipleItems(ids) {
    // form a GET request with action=delete_multiple
    // and the item ids as second argument
    window.location = compose_url("o=delete_multiple", 
            "items="+encodeURI(ids.toString()));
}
/* invoke a custom action */
function invokeAction(handler) {
    var ids = [];
    /* iterate through checked items and retrieve the object ids associated with each */
    $(".item-selection-checkbox:checked").each(function(index, elem) { 
        ids.push($(elem).data('pk'));
    });

    // special handling for deleting multiple items
    if (handler == '__delete_multiple_items')
        return deleteMultipleItems(ids);

    /* Submit the form after adding additional data - handler and object ids */
    var formAction = $("#id_form_action");
    formAction.attr('action', compose_url("o=action"));
    $('<input />').attr('type', 'hidden')
        .attr('name', 'handler')
        .attr('value', handler)
        .appendTo(formAction);
    $('<input />').attr('type', 'hidden')
        .attr('name', 'ids')
        .attr('value', ids.toString())
        .appendTo(formAction);
    formAction.submit();
}
/* invoke a custom item action */
function invokeCustomItemAction(key, item) {
    /* Submit the form after adding additional data - the custom 
     * action key and the selected object's id.
     */
    var formAction = $("#id_form_action");
    formAction.attr('action', compose_url("o=action", "item="+item));
    $('<input />').attr('type', 'hidden')
        .attr('name', 'handler')
        .attr('value', key)
        .appendTo(formAction);
    $('<input />').attr('type', 'hidden')
        .attr('name', 'id')
        .attr('value', item.toString())
        .appendTo(formAction);
    formAction.submit();
}
