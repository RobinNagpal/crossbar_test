import {Injectable} from "@angular/core";
import {Connection, IConnectionOptions, Session} from "autobahn";

@Injectable()
export class AutobahnService {

  connectToWamp(principalId: string, jwt_ticket: string) {
    // console.log("Ok, AutobahnJS loaded", autobahn.version);

    // this callback is fired during Ticket-based authentication
    //
    function onchallenge(session, method, extra) {

      console.log("onchallenge", method, extra);

      if (method === "ticket") {
        return jwt_ticket;

      } else {
        throw "don't know how to authenticate using '" + method + "'";
      }
    }

    const connection = new Connection({
      url: 'ws://127.0.0.1:8080/ws',
      realm: 'realm1',

      // the following attributes must be set for Ticket-based authentication
      //
      authmethods: ["ticket"],
      authid: principalId,
      onchallenge: onchallenge
    });

    connection.onopen = function (session, details) {

      console.log("connected session with ID " + session.id);
      console.log("authenticated using method '" + details.authmethod + "' and provider '" + details.authprovider + "'");
      console.log("authenticated with authid '" + details.authid + "' and authrole '" + details.authrole + "'");


      session.subscribe('com.crossbar_test.notification', function (args, kwargs) {
      }).then(
        function () {
          console.log("huh, function registered!");
        },
        function (err) {
          console.log("registration failed - this is expected", err);
        }
      );
    };

    connection.onclose = function (reason, details) {
      console.log("disconnected", reason, details.reason, details);
    };

    connection.open();
    console.log("opening new connection");

  }
}
