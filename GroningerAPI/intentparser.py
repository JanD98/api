from GroningerAPI.conversation_data import ConversationData
from GroningerAPI.dateformatter import DateFormatter
from GroningerAPI.models import Feedback
from GroningerAPI.moviefinder import MovieFinder
from GroningerAPI.parkingfinder import ParkingFinder

"""
context:
datetime
subject
genre
number
recommends
"""

class IntentParser:
    def parse(self, data, conversation):
        conversation_data = ConversationData(conversation.conversation_params)
        context = {'conversation': conversation}
        for key, value in conversation_data.__dict__.items():
            context[key] = value
        intent = '_default'
        if 'entities' in data:
            for key, value in data['entities'].items():
                if type(value) is list:
                    value = value[0]
                if key == 'intent':
                    intent = value['value']
                else:
                    context[key] = value['value']
        # todo: misschien hier na een paar keer menselijke help inroepen?
        result, context = getattr(self, intent)(context) or ['Ik kan je niet zo goed volgen, zou je me dit nog een keer kunnen vertellen?', context]
        for key, value in context.items():
            if key != 'conversation':
                setattr(conversation_data, key, value)
        conversation.conversation_params = conversation_data.to_json()
        conversation.save()
        return result

    def _default(self, context):
        if 'intent' in context and context['intent'] == 'reserve_movie' and 'number' in context:
            del context['intent']
            return self.reserve_movie(context)

    def yes(self, context):
        if 'intent' in context:
            if context['intent'] == 'continue_chat':
                return ['Waarmee kan ik je nog meer van dienst zijn?', []]
            intent = context['intent']
            del context['intent']
            return getattr(self, intent, lambda x: None)(context)

    def no(self, context):
        if 'intent' in context:
            if context['intent'] == 'continue_chat':
                return ['Mooi. Hopelijk kon ik je van dienst zijn. Mag ik je ten slotte nog vragen of je tevreden bent over dit gesprek?', []]
            elif context['intent'] == 'recommend_movie':
                return self.recommend_other(context)
            context['intent'] = 'continue_chat'
            return ['Ok, geen probleem. Kan ik nog iets anders voor je doen?', context]

    def find_something(self, context):
        return self.find_movie(context)

    def find_movie(self, context):
        if 'subject' in context:
            finder = MovieFinder(**context)
            time = finder.find_best_time()
            if not time:
                result = self.recommend_movie(context)
                result[0] = 'Helaas, ik kan ' + context['subject'] + ' niet vinden. ' + result[0]
                return result
            context['datetime'] = time
            context['intent'] = 'reserve_movie'
            return [context['subject'] + ' speelt ' + DateFormatter(time) + '. Zal ik tickets voor je reserveren?', context]
        else:
            return self.recommend_movie(context)

    def recommend_something(self, context):
        return self.recommend_movie(context)

    def recommend_movie(self, context):
        finder = MovieFinder(**context)
        context['recommends'] = finder.recommend_movies()
        if len(context['recommends']):
            context['subject'] = context['recommends'][0]
            return ['Misschien is ' + context['subject'] + ' wat voor je?', context]
        else:
            context['intent'] = 'continue_chat'
            return ['Helaas, ik kon niets voor je vinden. Kan ik misschien wat anders voor je doen?', context]

    def reserve_something(self, context):
        return self.reserve_movie(context)

    def reserve_movie(self, context):
        if 'subject' in context:
            finder = MovieFinder(**context)
            time = finder.find_best_time()
            if not time:
                result = self.recommend_movie(context)
                result[0] = 'Helaas, ik kan ' + context['subject'] + ' %(film)s niet vinden. ' + result[0]
                return result
            elif 'datetime' in context and time != context['datetime']['value']:
                old_time = context['datetime']
                context['datetime'] = time
                context['intent'] = 'reserve_movie'
                return [context['subject'] + ' speelt niet ' + DateFormatter(old_time) + ' maar wel ' + DateFormatter(time) + '. Wil je die misschien reserveren?', context]
            elif 'datetime' not in context:
                context['datetime'] = time
                context['intent'] = 'reserve_movie'
                return [context['subject'] + ' speelt ' + DateFormatter(time) + '. Wil je die reserveren?', context]
            if 'number' in context:
                if finder.reserve(context['number'], context['conversation'].user):
                    return ['Ik heb je reservering gemaakt. Je kan je tickets tot een kwartier van te voren ophalen bij de kassa.', {'intent': 'continue_chat'}]
                else:
                    context['intent'] = 'continue_chat'
                    return ['Helaas, zo veel plaatsen zijn er niet meer beschikbaar. Kan ik misschien iets anders voor je doen?', context]
            else:
                context['intent'] = 'reserve_movie'
                return ['Voor hoeveel personen mag ik een reservering maken?', context]
        else:
            return self.recommend_movie(context)

    def recommend_other(self, context):
        if 'intent' in context and context['intent'] == 'recommend_movie':
            if 'recommends' in context and len(context['recommends']) > 1:
                context['recommends'] = context['recommends'][1:]
                context['subject'] = context['recommends'][0]
                return ['Ok, misschien is ' + context['subject'] + ' meer wat voor je?', context]
            else:
                context['intent'] = 'continue_chat'
                return ['Ik ben bang dat ik niets meer heb om je aan te raden. Kan ik misschien wat anders voor je doen?', context]

    def accept_recommend(self, context):
        if 'intent' in context and context['intent'] == 'recommend_movie':
            context['intent'] = 'reserve_movie'
            return ['Leuk, zal ik die voor je reserveren?', context]

    def find_parking(self, context):
        finder = ParkingFinder(**context)
        count = finder.expected_spots()
        if count > 50:
            return ['Ja, dat is geen probleem. Kan ik nog wat anders voor je doen?', {'intent': 'continue_chat'}]
        elif count > 10:
            return ['Dat is denk ik geen probleem, maar het kan soms druk zijn. Kan ik nog wat anders voor je doen?', {'intent': 'continue_chat'}]
        elif count > 0:
            return ['Dat is heel krap. Ik kan niet beloven dat er nog plek zal zijn. Kan ik nog wat anders voor je doen?', {'intent': 'continue_chat'}]
        else:
            return ['Helaas, ik denk niet dat dat zal kunnen. Het is dan altijd heel druk. Kan ik misschien wat anders voor je doen?', {'intent': 'continue_chat'}]

    def review(self, context):
        if 'sentiment' in context and 'conversation_id' in context:
            if context['sentiment'] == 'positive':
                feedback = Feedback.objects.create(conversation=context['conversation'], rating=8)
                feedback.save()
                return ['Bedankt voor je feedback, hopelijk tot een volgende keer!', []]
            elif context['sentiment'] == 'negative':
                feedback = Feedback.objects.create(conversation=context['conversation'], rating=4)
                feedback.save()
                return ['Bedankt voor je feedback. Hopelijk kunnen we je een volgende keer beter van dienst zijn.', []]

    def find_restaurant(self, context):
        return self.information(context)

    def reserve_restaurant(self, context):
        return self.information(context)

    def information(self, context):
        return ['Je kan alle informatie over het Groninger Forum vinden op onze website www.groningerforum.nl. Kan ik iets anders voor je doen?', {'intent': 'continue_chat'}]

    def price_information(self, context):
        return self.information(context)
