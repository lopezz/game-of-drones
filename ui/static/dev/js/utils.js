
class BackendService {
    get(endpoint, callback) {
      $.get(endpoint, callback);
    }
  
    post(endpoint, data, callback) {      
      $.post(endpoint, data, callback);
    }

    createGame(data, callback) {
      this.post("/api/create_game/", data, this.toJS(callback));
    }
  
    registerRound(data, callback) {
      this.post("/api/register_round/", data, this.toJS(callback));
    }
  
    getScore(gameId, callback) {
      this.get("/api/get_score/?game_id=" + gameId, this.toJS(callback));
    }
  
    toJS(callback) {        
        return data => {
            const jsData = data; //JSON.parse(data); // TODO use this instead
            // const jsData = JSON.parse(data); // TODO use this instead
            callback(jsData);
        };      
    }
}

export default BackendService