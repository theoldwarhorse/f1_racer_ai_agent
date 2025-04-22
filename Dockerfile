FROM python:3
ENV TZ=Africa/Johannesburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt install -y python3 python3-pip

RUN mkdir /tmp/api/
WORKDIR /tmp/api/

COPY ./f1_agent.py ./
COPY ./f1_agent_visual.py ./
COPY ./README.md ./
COPY ./requirements.txt ./
COPY ./weekend_context_mock.json ./
COPY ./weekend_context_sample_1.json ./
COPY ./weekend_context_sample_2.json ./
COPY ./weekend_context.json ./
COPY ./large_language_models/ ./large_language_models/
COPY ./pages ./pages
COPY ./social_media_clients ./social_media_clients
COPY ./weekend_simulators ./weekend_simulators

RUN pip3 install -r requirements.txt

ENV token=123

EXPOSE 8501

CMD ["streamlit", "run", "f1_agent_visual.py", "--server.port=8501", "--server.address=0.0.0.0"]
