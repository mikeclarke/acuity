  function autoScroll(enabled) {    
    if (enabled == true) {
      if (this.scroll_fnId) return; // already running

      console.log("scroll ON!")
      this.scroll_fnId = setInterval( function(){
        $("#results").scrollTo( {top:'100%', left:'+=0'}, 300 );
      }, 1000 );
    } else {
      if (!this.scroll_fnId) return; 
      console.log("scroll off")
      if (this.scroll_fnId) {
        clearInterval(this.scroll_fnId);
        this.scroll_fnId = null;
      }
    }    
  }
