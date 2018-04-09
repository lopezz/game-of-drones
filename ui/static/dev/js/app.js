import React from 'react';
import ReactDOM from 'react-dom';
import BackendService from './utils'

const backendService = new BackendService(); 

class StartGameView extends React.Component {
  constructor() {
    super();
    this.submitForm = this.submitForm.bind(this);
    this.createGameResponse = this.createGameResponse.bind(this);
  }

  submitForm(e) {
    e.preventDefault();
    const data = $(e.target).serialize();
    backendService.createGame(data, this.createGameResponse);
  }

  createGameResponse(data) {
    const gameId = data.game_id;
    const players = [this.player1.value, this.player2.value];
    this.props.onCreateGameResponse(gameId, players);
  }

  render() {
    return (
      <form onSubmit={this.submitForm}>
        <div className="row">
          <div className="col-md-12">
            <h1>Enter Player's names</h1>
          </div>
        </div>
        <div className="row">
          <div className="col-sm-3">
            <label>Player 1</label>
          </div>
          <div className="col-sm-9">
            <input
              name="player1"
              ref={e => (this.player1 = e)}
              type="text"
              maxLength="10"
            />
          </div>
        </div>

        <div className="row">
          <div className="col-sm-3">
            <label>Player 2</label>
          </div>
          <div className="col-sm-9">
            <input
              name="player2"
              ref={e => (this.player2 = e)}
              type="text"
              maxLength="10"
            />
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <br />
            <input className="submit-btn" type="submit" value="Start" />
          </div>
        </div>
      </form>
    );
  }
}

class GameRoundView extends React.Component {
  constructor(props) {
    super(props);
    this.onSubmitForm = this.onSubmitForm.bind(this);
  }
  onSubmitForm(e) {
    e.preventDefault();
    const move = this.select.value;
    this.props.onMove(this.getCurrentPlayerIdx(), move);
    this.form.reset();
  }

  getCurrentPlayerIdx() {
    const { currentMoves } = this.props;
    return currentMoves.length && currentMoves[0] ? 1 : 0;
  }

  render() {
    const { rounds, players } = this.props;
    const roundNumber = rounds && rounds.length + 1;
    const currentPlayer = players[this.getCurrentPlayerIdx()];
    const playerName = currentPlayer;
    return (
      <form onSubmit={this.onSubmitForm} ref={e => (this.form = e)}>
        <div className="row">
          <div className="col-md-12">
            <h1>Round {roundNumber}</h1>
          </div>

          <div className="col-md-6">
            <h2>{playerName}</h2>
            Select move:{" "}
            <select name="move" ref={e => (this.select = e)}>
              <option selected value="rock">
                Rock
              </option>
              <option value="paper">Paper</option>
              <option value="scissors">Scisorss</option>
            </select><br/>
            <input type="submit" value="Ok" />
          </div>

          <div className="col-md-6">
            <GameScore rounds={rounds} />
          </div>
        </div>
      </form>
    );
  }
}

class GameScore extends React.Component {
  render() {
    const { rounds } = this.props;
    if (!rounds.length) {
      return null;
    }

    return (
      <div className="score-table">
        <h2>Score</h2>
        <table>
          <thead>
            <tr>
              <th>Round</th>
              <th>Winner</th>
            </tr>
          </thead>
          <tbody>
            {rounds.map(r => (
              <tr key={r.round_no}>
                <td>{r.round_no}</td>
                <td>{r.round_winner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}

class GameEndedView extends React.Component {
  render() {
    const { winner, onButtonClick } = this.props;
    return (
      <div>
        <h1>We have a WINNER!</h1>
        {winner} is the new EMPEROR!<br />
        <button onClick={onButtonClick}>Play again</button>
      </div>
    );
  }
}

const [NEW, PLAYING, ENDED] = [1, 2, 3];


class Game extends React.Component {
  constructor() {
    super();
    this.initialState = {
      rounds: [],
      currentMoves: [],
      players: [],
      gameId: 0,
      winner: null
    };
    this.state = Object.assign({}, this.initialState);
    this.createGame = this.createGame.bind(this);
    this.onMove = this.onMove.bind(this);
    this.onRegisterRound = this.onRegisterRound.bind(this);
    this.onGetScore = this.onGetScore.bind(this);
    this.reset = this.reset.bind(this);
  }

  getGameStatus() {
    const { gameId, winner } = this.state;
    if (!gameId) {
      return NEW;
    } else if (gameId && !winner) {
      return PLAYING;
    }
    return ENDED;
  }

  createGame(gameId, players) {
    this.setState({ gameId, players, currentMoves: [], rounds: [] });
  }

  onMove(playerIdx, move) {
    const { currentMoves, gameId } = this.state;
    let newCurrentMoves;
    if (!playerIdx) {
      //player 1
      newCurrentMoves = [move];
      this.setState({ currentMoves: newCurrentMoves });
    } else {
      newCurrentMoves = currentMoves.concat([move]);
      const [player1_move, player2_move] = newCurrentMoves;
      const data = { game_id: gameId, player1_move, player2_move };
      backendService.registerRound(data, this.onRegisterRound);
    }
  }

  onRegisterRound(response) {
    //TODO evaluate success
    const { gameId } = this.state;
    const { success, winner } = response;
    if (!winner) {
      backendService.getScore(gameId, this.onGetScore);
    }
    this.setState({ winner });
  }

  onGetScore(response) {
    const rounds = response.game_rounds;
    this.setState({ rounds, currentMoves: [] });
  }

  reset() {
    this.setState(Object.assign({}, this.initialState));
  }

  render() {
    const { gameId, currentMoves, rounds, players, winner } = this.state;
    const gameStatus = this.getGameStatus();

    return (
      <div className="container">
        {gameStatus === NEW && (
          <StartGameView onCreateGameResponse={this.createGame} />
        )}
        {gameStatus === PLAYING && (
          <GameRoundView
            currentMoves={currentMoves}
            players={players}
            rounds={rounds}
            onMove={this.onMove}
          />
        )}
        {gameStatus === ENDED && (
          <GameEndedView winner={winner} onButtonClick={this.reset} />
        )}
      </div>
    );
  }
}

ReactDOM.render(<Game />, document.querySelector("#app"));