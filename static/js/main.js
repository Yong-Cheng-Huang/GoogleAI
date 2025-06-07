$(function(){
    $("#submit").click(chatWithLLM);
    $("#message").keypress(function(e){
        if(e.which == 13){
            chatWithLLM();
        }
    });
});

function chatWithLLM(){
    var message = $("#message").val();
    if (message.trim() === "") return;
    
    var userMessageDiv = $("<div>").addClass("message user-message").text(message);
    $("#dialog").append(userMessageDiv);
    
    var data = {
        message: message
    };
    
    $.post("/call_llm", data, function(data){
        var aiMessageDiv = $("<div>").addClass("message ai-message").text(data);
        $("#dialog").append(aiMessageDiv);
        $("#dialog").scrollTop($("#dialog")[0].scrollHeight);
    });
    
    $("#message").val("");
    $("#dialog").scrollTop($("#dialog")[0].scrollHeight);
}