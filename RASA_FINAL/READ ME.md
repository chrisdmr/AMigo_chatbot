**AMigo: An new integrated morning assistant chatbot**  

**By Christina Doumoura**

**Identification, domain, and motivation**

AMigo is a morning update chatbot that can help summarize your morning and get you ready for the day in no time. This chatbot is developed in the domain of daily personal assistance, focusing specifically on providing users with all the insight they need for a seamless start to their day.   
In today’s fast-paced world, individuals have limited time in the mornings to catch up with all the information that is necessary for their daily planning. They also often find that they don’t want to spend too much time thinking about mundane tasks, such as modifying their outfits or their activities according to the weather and that they would prefer tailor-made propositions. Now, instead of wasting precious time on visiting multiple different apps on their phone to check different kinds of news and the weather and on curating the perfect outfit or activity, they can just ask AMigo\! The goal of AMigo’s task integration is to let the busy everyman dedicate more time on what truly matters, by streamlining their daily tasks.

**How to run AMigo**  
After downloading RASA, the country\_converter library, and python 10, one must open Command Line and run the command sequence  
`cd C:\Users\[user name]\Desktop\rasa`  
`C:\Users\[user name]\rasa_env\Scripts\activate`  
to activate the rasa environment. Then, they can run   
`C:\Users\nickm\rasa_env\Scripts\python.exe -m rasa train`  
if they wish to train the model using the latest code updates. After that, one must open a new Command Line window and run  
`cd C:\Users\nickm\Desktop\rasa`  
`C:\Users\nickm\rasa_env\Scripts\activate`  
`C:\Users\nickm\rasa_env\Scripts\python.exe -m rasa run actions`  
so as to run AMigo’s actions and initiate a debugging environment. Finally, in yet another Command Line window, they must run  
`cd C:\Users\nickm\Desktop\rasa`  
`C:\Users\nickm\rasa_env\Scripts\activate`  
`C:\Users\nickm\rasa_env\Scripts\python.exe -m rasa shell`  
to open the chat interface. Have fun\!

**Descriptions of the implemented scenarios and how they demonstrate the chatbot’s functionalities**

AMigo supports multiple distinct interaction scenarios, each representing a different user goal:

#### **Scenario 1: Weather-based activity recommendation (Mock task)**

In this scenario, the user asks the chatbot to tell them what the weather is like. Then, they can ask it to recommend an activity that is suitable for these weather conditions.

* At first, the chatbot picks one random weather condition from a predefined list (snowy, sunny, rainy)

* Based on the weather condition it picked, it can then recommend appropriate indoor or outdoor activities (e.g.,reading a book, going for a walk, visiting a coffee shop) from a predefined dictionary.

This scenario highlights:

* The chatbot’s core dialog management capabilities, including custom action execution, conditional logic, and response generation.

* AMigo’s slot management abilities, such as slot filling, storing, and carryover. 

* AMigo’s context awareness, as it demonstrates its state tracking abilities by “remembering” what weather conditions it randomly picked the first time it was asked about the weather and restates them if asked to do so across subsequent interactions. 

* The chatbot’s ability to dynamically generate responses based on stored slot values rather than static templates.

#### **Scenario 2: Outfit Recommendation according to real life API weather data in a given city**

In this scenario, the user asks AMigo to recommend an outfit for them to wear. If they don’t mention the city they are interested in, the chatbot will ask them to provide it. 

* The user requests outfit ideas. They are free to either provide their city they are located at on their turn or wait for the chatbot to ask them about it.

* If they provided a city, the chatbot will fetch real-time weather data for that specified city using a weather API. If they did not, AMigo will first request that they provide it and then proceed to the aforementioned step.

* Based on the city’s temperature, weather conditions, and chance of precipitation, the chatbot recommends suitable clothing (e.g., light clothing, jacket, umbrella).

This scenario demonstrates:

* Slot filling, extraction, and validation. The chatbot extracts the city name from user input and validates its presence before proceeding. If the required slot is missing, the chatbot prompts the user to re-enter its value.

* Integration with a real-world data source (External API)**.** The chatbot retrieves real-time weather data from an external online weather service based on the city the user provided.

* Dynamic response generation based on external data. The data extracted from the API interacts with the data included in the chatbot’s code, so as to provide each user with a personalized outfit suggestion.  
* Data Parsing and Processing: The chatbot processes structured JSON responses from the API, extracting relevant information such as temperature and weather conditions.

* Error Handling and Robustness. Network failures, invalid city names, or unexpected API errors are dealt with via exception handling, ensuring the chatbot provides meaningful feedback instead of failing silently.

* Conversation State Management. The slots are explicitly reset after the completion of a turn exchange, to prevent old information from affecting future interactions with new user input.

#### **Scenario 3: Top news headlines by category and country**

In this scenario, the chatbot provides a personalized morning news briefing based on the user’s specified country and news category.

* The user asks AMigo for a news update on a specific category (e.g., technology, sports, business) in a specific country.

* The chatbot dynamically retrieves the top 3 relevant headlines from a news API and lists them in the user interface.

This scenario demonstrates:

* Integration with a second real-world data source and multiple parameter handling. The chatbot retrieves data from the news API by extracting 2 separate entities from 1 single user input, thus managing multiple slots simultaneously.

* Data Normalization and Preprocessing: The chatbot converts the user-provided country names into standardized ISO country codes, enabling reliable interaction with the external API.

* Slot validation and standardization via internal library mapping dataset. By using a country//country code dataset within the country\_converter library, AMigo manages to handle variations in user input (e.g., “USA”, “United States”, “US”) and validate that the geopolitical entity that the user provides is, in fact, a country.

* Fallback Logic Application. If the user fails to provide AMigo with a specific news category or if AMigo fails to recognise the category input, it does not fail silently, but rather decides to fetch the top 3 most important news titles from the specified country, regardless of category.

* Robust Error Handling: Invalid inputs, missing slots, or unexpected API responses are handled gracefully, as the user is presented with informative feedback.


  
**Details about the integrated data sources and their rationale**.

#### **Weather data source**

AMigo uses the **wttr.in** API service to retrieve live weather information for user-specified cities. This API was chosen because it provides current weather conditions in an easily retrievable JSON-based format, without requiring further authentication, making it suitable for this task of educational and gradable nature.

#### **News data source**

As for the morning news briefing scenario, AMigo integrates with the **NewsData.io** API to retrieve the top 3 news headlines in a specific country and category. This API was selected due to its broad international news coverage and category-based filtering, both of which enable personalized news delivery. Furthermore, its simple https format, which includes the selected country code and news category, allows for easier incorporation into the code, interaction with the country\_converter dataset, and simpler debugging.

**Challenges faced during implementation and how they were addressed**

During the development of AMigo, several dialogue management, slot handling, entity recognition, and external API related challenges arose. The following section describes these very challenges, as well as the approaches used to address them.

1. Slot resetting in API based tasks  
   Challenge:  
   Slots that had already been filled once during interactions with an API (e.g., city, country, category) persisted across turns where the user provided different values than they did the first time, leading to unintended reuse of outdated information and mismatched question-answer pairs in subsequent interactions.  
   Solution:  
   The explicit implementation of slot resetting was deemed necessary after the completion of each task in all API-based actions. Relevant slots are emptied once a response is delivered (via return \[SlotSet(key:, None)\], ensuring that each new user request is processed independently and and solidifying the user’s ability to make requests about multiple cities/countries/news categories.   
2. Overly aggressive fallback threshold  
   Challenge:

The default core\_fallback\_threshold value of 0.3 caused the dialogue manager to be overly cautious and falsely trigger fallback actions, even when user intents had been correctly understood. This resulted in unnecessary conversation interruptions.

Solution:

After several trials, the core\_fallback\_threshold was increased to 0.76. This adjustment reduced excessive fallback triggering, allowing for a much smoother conversation flow by increasing the dialogue manager’s confidence.

3. Country and city recognition in user input  
   Challenge:  
   The accurate recognition and extraction of the country and city names from the user input proved to be quite difficult. The first attempts involved the manual listing of various countries and cities in the NLU training data, with the hope that the system would learn to generalise and recognise such entities. However, this approach did not scale well and caused issues with multi-word entities (e.g., “Rio de Janeiro, New York”), as sometimes only part of the entity name got recognised (once the user asked for an outfit suggestion for New York, USA, and got a suggestion for York, UK instead), and as, occasionally, there were some issues with the city formatting, which needed to be very specific, so that the API URL would be valid.   
   Solution:   
   The approach that ended up being the best by far was using SPACY’s pretrained Named Entity Recognition (NER) model, which reliably identifies Geo-Political Entities (GPE). This significantly improved the recognition of multi-word entities and dramatically reduced the need for extensive manual training examples.  
4. Category constraints in the news API   
   Challenge:  
   The news API only supports a predefined set of news categories. As such, there was a need to include a closed list of categories, which would be the only categories AMigo would recognise. If the user requested the news on some other domain, they would be informed that this specific category is invalid and that they will be presented with the overall top 3 news headlines instead..   
   Solution:  
   An exclusive lookup table was introduced for the category slot, thus restricting user input to API supported categories.   
5. Country validation and standardization  
   Challenge:  
   Even though SPACY is quite successful at extracting GPE entities, not all extracted entities correspond to valid countries supported by the news API (if not country is *technically* if not GPE)  
   Solution:  
   The key to resolving this conundrum was the utilization of the country\_converter library, which even proved to be a double blessing in disguise. Not only did it try mapping the names of the extracted GPE entities to standardized ISO2 codes, thereby proving their country status if successful, but it also helped fill the country code variable in the API URL, while also accounting for different kinds of country name variants (e.g., United States of America, United States, USA). This method effectively narrows down user values to legitimate countries only.  
   A similar approach is used for city names. However, fewer issues were encountered here, due to the broader geographic coverage of the weather API. It is however worth noting that, even though the user intent in the outfit recommendation action is to be presented with an outfit according to the weather in a specific city, the action is executable with any kind of GPE entry that [wttr.in](http://wttr.in) has meteorological data on, as the detection of a method to cross check the GPE’s city status was not possible at this time.  
6. Activity recommendations without prior weather context  
   Challenge:  
   Users have the freedom to ask AMigo to recommend an activity according to the weather conditions, without having explicitly asked it about the weather yet, which could cause the weather slot to be empty.  
   Solution:   
   When weather information is unavailable, AMigo implements random weather selection by using random.choice, as it does during the “normal” pipeline (where the user first inquires about the weather and then requests an activity). This ensures the full functionality of the interaction, even in the absence of prior context.  
7. Simulated vs API task slot management  
   Challenge:   
   The mock task and the real API integration tasks required different slot management strategies, as, in contrast to the latter, the mock task’s internal logic and state management benefited from slot persistence.  
   Solution:   
   The slot handling strategy was differentiated, as the weather slot is set once and is then used recursively in the mock action, while API-based tasks explicitly empty relevant slots after execution.  
8. Pipeline modifications for improved robustness  
   Challenge:

The default configuration pipeline was not optimal for entity extraction, Named Entity Recognition and constrained user inputs.

Solution:

The pipeline was modified to include lookup tables, SPACY and SPACY Entity Extractor, and Regex Entity Extractor. These changes significantly enhanced AMigo’s ability to handle natural language user input in a sometimes more flexible and sometimes more controlled manner.

**Instructions for setting up keys, credentials, or environment variables required for accessing the data sources.**

This chatbot utilizes external data sources that require minimal configuration. The [wttr.in](http://wttr.in) API has been chosen specifically for its ease of use. The only credential required is the API key for [NewsData.io](http://NewsData.io), which is included in [actions.py](http://actions.py) and used via its assigned variable api\_key when accessing the API address. The country\_converter library only needs to be installed before it is accessed via a direct import as cc within the codebase. 

**Example runs to showcase implemented functionalities.**

!(screenshots/1.png)

This run of the first mock action showcases the AMigo’s ability to manage the required persistence of the conversational state, execute custom actions, apply conditional lo  
gic, and maintain context across multiple turns, without relying on external data sources.

---

!(screenshots/2.png)
!(screenshots/3.png)

As we can see in the debugging process, even though the chatbot processed the user input correctly and filled the API URL accordingly, the API failed to fetch the required data and the request timed out. Here, we can observe AMigo’s capability at handling errors, such as network timeouts and API failures, in a graceful manner and at ensuring its uninterrupted interaction and conversation continuation.

(P.S.: Since this screenshot was taken, the error message for this situation has been updated to “Sorry, I couldn't check the weather and recommend an outfit right now. Maybe try again later?”)  

---

!(screenshots/4.png)

As observed, AMigo does not recognise the “incorrect” spelling of hello, but that does not stop it from informing the user accordingly and continuing the conversation. This highlights the chatbot’s proper fallback structure and logic.  
---
!(screenshots/5.png)

This run demonstrates AMigo’s ability to switch between different slots regarding multiple entities at the same time, as well as its country recognition skills (Yugoslavia used to be a country, but there’s obviously no corresponding country code in the coco library anymore, so it declares it invalid.)  
---

!(screenshots/6.png)
!(screenshots/7.png)

This chat demonstrates the chatbot’s ability to recognize diverse news-related intents, extract and validate country and category entities, and dynamically retrieve the top 3 relevant headlines by an external news API. It also highlights AMigo’s robust slot management, including category fallback handling, controlled validation of invalid country inputs, and slot resetting between turns. The system also successfully handles invalid and missing values in a differentiated way, as it can’t fetch the news if no country is provided, but it decides to just list the overall top 3 news headlined if no category is provided instead, highlighting the flexibility of the fallback system.  
---

!(screenshots/8.png)

This specific run demonstrates AMigo’s ability to provide personalized outfit recommendations by correctly identifying the user’s request, extracting and validating the city slot, and prompting the user to provide additional info when necessary. It dynamically generates clothing suggestions according to the temperature and the overall weather conditions in a given city. The functionalities that are highlighted here are error handling and GPE recognition, as AMigo realizes when the user fails to mention their city of interest and requests that they do so, and conversation state management, as all slots are reset after each turn to prevent old information from affecting future interactions. We can also observe that AMigo has no problem handling multi-word city entities, therefore demonstrating its successful text preprocessing skills. Overall, the run showcases AMigo’s conditional logic, personalization, and robust slot management when recommending weather-conscious outfits.  
