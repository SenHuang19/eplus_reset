#FROM senhuang/jmodelica

#FROM michaelwetter/ubuntu-1604_jmodelica_trunk

FROM senhuang/pyfmi
USER root

MAINTAINER Sen


ENV ROOT_DIR /usr/local
ENV JMODELICA_HOME $ROOT_DIR/JModelica
ENV IPOPT_HOME $ROOT_DIR/Ipopt-3.12.4
ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV PYTHONPATH $PYTHONPATH:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica


ENV ENERGYPLUS_VERSION 8.5.0
ENV ENERGYPLUS_TAG v8.5.0
ENV ENERGYPLUS_SHA c87e61b44b

ENV ENERGYPLUS_INSTALL_VERSION 8-5-0

ENV ENERGYPLUS_DOWNLOAD_BASE_URL https://github.com/NREL/EnergyPlus/releases/download/$ENERGYPLUS_TAG
ENV ENERGYPLUS_DOWNLOAD_FILENAME EnergyPlus-$ENERGYPLUS_VERSION-$ENERGYPLUS_SHA-Linux-x86_64.sh
ENV ENERGYPLUS_DOWNLOAD_URL $ENERGYPLUS_DOWNLOAD_BASE_URL/$ENERGYPLUS_DOWNLOAD_FILENAME

RUN curl -SLO $ENERGYPLUS_DOWNLOAD_URL \
    && chmod +x $ENERGYPLUS_DOWNLOAD_FILENAME \
    && echo "y\r" | ./$ENERGYPLUS_DOWNLOAD_FILENAME \
    && rm $ENERGYPLUS_DOWNLOAD_FILENAME \
    && cd /usr/local/EnergyPlus-$ENERGYPLUS_INSTALL_VERSION \
    && rm -rf DataSets Documentation ExampleFiles WeatherData MacroDataSets PostProcess/convertESOMTRpgm \
    PostProcess/EP-Compare PreProcess/FMUParser PreProcess/ParametricPreProcessor PreProcess/IDFVersionUpdater

# Remove the broken symlinks
RUN cd /usr/local/bin \
    && find -L . -type l -delete

RUN ["ln", "-s", "/usr/local/EnergyPlus-8-5-0/Energy+.idd", "/usr/local/Energy+.idd"]

RUN pip install --user pandas

RUN pip install --user matplotlib

ADD Resets /home/developer/fmu/Resets

ADD reset_default_results /home/developer/fmu/reset_default_results

ADD baseline_results /home/developer/fmu/baseline_results

ADD configs /home/developer/fmu/configs

ADD run.config /home/developer/fmu/

ADD *.fmu /home/developer/fmu/

ADD *.py /home/developer/fmu/