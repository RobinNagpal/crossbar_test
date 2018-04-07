import {Injectable} from "@angular/core";
import {Connection, Session, IConnectionOptions} from "autobahn";

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

      // call a procedure we are allowed to call (so this should succeed)
      //
      session.call('com.example.add2', [2, 3]).then(
        function (res) {
          console.log("call result", res);
        },
        function (error) {
          console.log("call error", error);
        }
      );

      // (try to) register a procedure where we are not allowed to (so this should fail)
      //
      session.register('com.example.mul2', function (args, kwargs) {
      })
        .then(
          function () {
            console.log("huh, function registered!");
          },
          function (err) {
            console.log("registration failed - this is expected", err);
          }
        );

      // publish to some topics we are allowed to publish to.
      //
      var allowed_topics = [
        'com.example.topic1',
        'com.foobar.topic1'
      ];

      for (var i = 0; i < allowed_topics.length; ++i) {

        (function (j) {
          session.publish(allowed_topics[j], ['hello'], null, {acknowledge: true})
            .then(
              function (pub) {
                console.log("event published to topic", allowed_topics[j]);
              },
              function (err) {
                console.log("publication to topic " + allowed_topics[j] + " failed", err);
              }
            );
        })(i);
      }

      // (try to) publish to some topics we are not allowed to publish to (so this should fail)
      //
      var disallowed_topics = [
        'com.example.topic2',
        'com.foobar.topic2'
      ];

      for (var i = 0; i < disallowed_topics.length; ++i) {

        (function (j) {
          session.publish(disallowed_topics[j], ['hello'], null, {acknowledge: true})
            .then(
              function (pub) {
                console.log("event published to topic", disallowed_topics[j]);
              },
              function (err) {
                console.log("publication to topic " + disallowed_topics[j] + " failed - this is expected", err);
              }
            );
        })(i);
      }

    };

    connection.onclose = function (reason, details) {
      console.log("disconnected", reason, details.reason, details);
    }

    connection.open();
    console.log("opening new connection");

  }
}
