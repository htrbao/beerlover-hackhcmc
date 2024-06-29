import backoff
import json
from typing import Optional

from services.beer_vlm.logger import LogManager
from services.beer_vlm.language_model import AbstractLanguageModel
from .abstract_prompter import AbstractPrompter


class BackgroundPrompter(AbstractPrompter):
    def __init__(self, lm: AbstractLanguageModel, name="background"):
        system_prompt = """
You are expert in identifying the location of the images.
All of your answer should be based on the image do not make up anything.

You only need to be choose a single location from this list of locations: restaurant, supermarket, bar, pub, brewery, liquor store, convenience store, grosary store, beer festival, private house, hotel, sports stadium, concert venue, airport lounge, cruise ship, nightclub, cafeteria, train station kiosk, food truck, beach resort, market, backyard BBQ, camping site, house party, street restaurant, beer event, celebration, gathering.

Then you need to identify the activity of the location in image from this list of actitivies: drinking, socializing, playing darts, playing pool, watching sports, listening to live music, dining, conversing, celebrating special occasions, tasting new dishes, shopping, comparing products, browsing, checking out, selecting beverages, asking for recommendations, purchasing, picking up snacks and drinks, paying, browsing, touring the facility, tasting beer samples, learning about brewing processes, buying beer merchandise, sampling various beers, attending workshops, socializing, listening to live music, watching games, cheering for teams, eating, watching performances, dancing, singing along, waiting for flights, checking in, going through security, using amenities, listening to DJs, reading, working, ordering food, gambling, playing slot machines, attending shows, attending events, riding attractions, playing games, playing golf, refueling vehicles, buying snacks, buying drinks, using restrooms, swimming, sunbathing, participating, relaxing, attending classes, studying, participating, selling, talking, smiling, setup the point of sales material.

After identifying the location, you need to identify at least 1 and at most 3 atmospheres of this location based on this list of asmospheres: social, noisy, casual, formal, welcoming, busy, practical, utilitarian, focused, well-organized, quick, straightforward, cramped, craft-oriented, communal, industrial-chic, festive, crowded, vibrant, energetic, loud, competitive, electric, immersive, transitional, calm, hectic, comfortable, luxurious, high-energy, dark, light, cozy, intimate, bustling, outdoors, glamorous, tense, fun, serene, leisurely, expansive, relaxed, tropical, lively, neutral.

Finally, you need to identify at least 1 and at most 3 emotions of this location based on this list of emotions: joyful, friendly, relaxed, content, satisfied, social, neutral, efficient, rushed, anticipation, excitement, decisive, spontaneous, enthusiastic, appreciative, joyous, passionate, communal, thrilled, engaged, anxious, bored, secure, lively, calm, comfortable, hopeful, adventurous, focused, hurried, convenient, happy, carefree, excited, curious, enjoyable.

You answer should be the JSON format, example:
{
    "location": "identified location of image",
    "activity": "identified activity of image",
    "atmosphere": ["first atmosphere of image",...],
    "emotion": ["first emotion of image",...],
}
        """
        self.background_prompt = """
Answer the location, atmosphere and emotion of image in JSON format.
"""
# - People who are appearing in the background that could be customers, promotion peoples, etc. If promotion people are in the background, you should describe about logo or brand on their image which beer they are promoting.

        super(BackgroundPrompter, self).__init__(lm, system_prompt, name=name)
        
    def require_prompters(self) ->set[str]:
        require_list = []
        return set(require_list)
    
    
    async def default_background(self):
        return {
            "location": "unknown",
            "activity": "unknown",
            "atmosphere": ["neutral"],
            "emotion": ["neutral"],
            "prompt": self.background_prompt_prepare(),
        }
    
    async def background_prompt_prepare(self, location="unknown", activity="unknown", atmosphere=["neutral"], emotion=["neutral"]):
        return f"image of a {location} with a {', '.join(atmosphere)} atmosphere, evoking feelings of {', '.join(emotion)}, where people are {activity}."
    
    # @backoff.on_exception(backoff.expo, exception=Exception,max_time=5, max_tries=2)
    async def handle_background(self, image: Optional[str], **results) -> dict:
        query_prompt = self.background_prompt
        answer = await self.lm.query(query_prompt, image, 1, self.system_prompt)
        answer = await self.lm.get_response_texts(answer)
        answer = answer[0]
        
        answer = json.loads(answer)
        answer["prompt"] = await self.background_prompt_prepare(**answer)
        return answer
    async def query(self, image: Optional[str], **results) -> str:
        # return self.handle_background(image, **results)
        try:
            return await self.handle_background(image, **results)
        except:
            return await self.default_background()