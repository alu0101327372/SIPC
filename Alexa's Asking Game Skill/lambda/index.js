/* *
 * This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK (v2).
 * Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
 * session persistence, api calls, and more.
 * */
const Alexa = require('ask-sdk-core');

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle(handlerInput) {
      //  return GetFactIntentHandler.handle(handlerInput);
       const speakOutput = 'Bienvenido, si quieres saber curiosidades sobre la NBA solo tienes que preguntar.';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

const GetNewFactIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'GetNewFactIntent'
                || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.YesIntent';
    },
    handle(handlerInput) {
        const speakOutput = RandomItem(CURIOSIDADES);

        return handlerInput.responseBuilder
            .speak(speakOutput + RandomItem(PREGUNTAS))
            .reprompt(speakOutput)
            .getResponse();
    }
};

const HelpIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'Que necesitas saber.';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && (Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.CancelIntent'
                || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.StopIntent'
                 || Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.NoIntent');
    },
    handle(handlerInput) {
        const speakOutput = 'Adiós, hasta pronto.';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};
/* *
 * FallbackIntent triggers when a customer says something that doesn’t map to any intents in your skill
 * It must also be defined in the language model (if the locale supports it)
 * This handler can be safely added but will be ingnored in locales that do not support it yet 
 * */
const FallbackIntentHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'AMAZON.FallbackIntent';
    },
    handle(handlerInput) {
        const speakOutput = 'Lo siento, no sé nada de eso. Inténtalo de nuevo.';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};
/* *
 * SessionEndedRequest notifies that a session was ended. This handler will be triggered when a currently open 
 * session is closed for one of the following reasons: 1) The user says "exit" or "quit". 2) The user does not 
 * respond or says something that does not match an intent defined in your voice model. 3) An error occurs 
 * */
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        console.log(`~~~~ Session ended: ${JSON.stringify(handlerInput.requestEnvelope)}`);
        const speakOutput = 'Lo siento, ha ocurrido un error. Vuelva a intentarlo de nuevo';
         return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

/**
 * Generic error handling to capture any syntax or routing errors. If you receive an error
 * stating the request handler chain is not found, you have not implemented a handler for
 * the intent being invoked or included it in the skill builder below 
 * */
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        const speakOutput = 'Lo siento, tuve problemas para hacer lo que me pediste. Inténtalo de nuevo.';
        console.log(`~~~~ Error handled: ${JSON.stringify(error)}`);

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

function RandomItem(array) { // <--- necessary to obtain a random element of an array
    return array[Math.floor(Math.random()*array.length)]
}

const CURIOSIDADES = [
    
    'Con 1.60 metros de altura Muggsy Bogues fue el jugador de menor estatura en pertenecer a la NBA. Fue elegido por los Washington Bullets donde compartió equipo con Manute Bol de 2.31 metros. ',
    'Desde 1946 existen los Knicks y Celtics, y son las franquicias más longevas si tomamos en cuenta que no han sufrido ningún cambio de nombre ni de ciudad. ',
    'La silueta que aparece en el logo de la NBA es Jerry West, legendario jugador de los Lakers quien estuvo cerca de nunca ganar un campeonato. ',
    'Shaquille O’Neal y Kareem Abdul-Jabbar solo anotaron 2 triples entre los dos.',
    'El 17 de diciembre de 1991, los Cavaliers se enfrentaron al Heat con un resultado final de 148 a 80 a favor de los Cavs. Es el récord de victoria por mayor diferencia de puntos en un partido. ',
    'A la edad de 22 años, Derrick Rose fue el más joven en ser nombrado el Jugador Más Valioso en la historia de la NBA. ',
    'En la campaña 2015-2016, Stephen Curry se convirtió en el único en ser nombrado el Jugador Más Valioso de forma unánime. ',
    'Con 11 campeonatos, Bill Russell es el jugador con más campeonatos en la historia de la NBA. ',
    'Desde 1984 el trofeo que se otorga al campeón lleva el nombre de Larry O’Brien, quien fuera comisionado de la NBA entre 1975 y 1984. ',
    'Uno de los mejores en la historia fue seleccionado en la posición 13 del Draft de 1996. Por si no fuera increíble que 13 equipos ignoraron a Kobe Bryant, el equipo que lo seleccionó no fue Lakers (con quienes jugaría 16 años), sino los Charlotte Hornets. ',
    ];
    
const PREGUNTAS = [
    
    'Qué más quieres saber? ',
    'Quiere saber algo más? ',
    'Quiere continuar? ',
    'Le gustaria saber más? ',
    'Te digo otra? ',
    ];

/**
 * This handler acts as the entry point for your skill, routing all request and response
 * payloads to the handlers above. Make sure any new handlers or interceptors you've
 * defined are included below. The order matters - they're processed top to bottom 
 * */
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        GetNewFactIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        FallbackIntentHandler,
        SessionEndedRequestHandler)
    .addErrorHandlers(
        ErrorHandler)
    .lambda();