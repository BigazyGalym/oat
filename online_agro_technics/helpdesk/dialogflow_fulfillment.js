'use strict';

const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const axios = require('axios');

process.env.DEBUG = 'dialogflow:debug';

exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });

  function welcome(agent) {
    agent.add(`Здравствуйте! Добро пожаловать в техническую поддержку AgroTechnics!`);
  }

  function fallback(agent) {
    agent.add(`Извините, я не понял ваш запрос. Попробуйте еще раз.`);
  }

  async function createTicket(agent) {
    const title = agent.parameters.title || 'Новый тикет';
    const description = agent.parameters.description || 'Без описания';
    const service_type_id = agent.parameters.service_type_id;

    try {
      const response = await axios.post(
        'http://localhost:8000/helpdesk/api/tickets/create/',
        {
          title,
          description,
          service_type: service_type_id,
        },
        {
          headers: { Authorization: `Token 54b909b97aa6cdc02e1b3906b2dbd618a6e3c7d0` }
        }
      );
      agent.add(`Тикет успешно создан: ${response.data.title} (ID: ${response.data.id})`);
    } catch (error) {
      agent.add(`Ошибка при создании тикета: ${error.message}`);
    }
  }

  async function listTickets(agent) {
    try {
      const response = await axios.get(
        'http://localhost:8000/helpdesk/api/tickets/',
        {
          headers: { Authorization: `Token 54b909b97aa6cdc02e1b3906b2dbd618a6e3c7d0` }
        }
      );
      const tickets = response.data;
      if (tickets.length === 0) {
        agent.add('У вас нет тикетов.');
      } else {
        let message = 'Ваши тикеты:\n';
        tickets.forEach(ticket => {
          message += `- ${ticket.title} (${ticket.status})\n`;
        });
        agent.add(message);
      }
    } catch (error) {
      agent.add(`Ошибка при получении тикетов: ${error.message}`);
    }
  }

  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('Create Ticket', createTicket);
  intentMap.set('List Tickets', listTickets);
  agent.handleRequest(intentMap);
});