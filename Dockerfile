FROM opensearchproject/opensearch:3.0.0
RUN /usr/share/opensearch/bin/opensearch-plugin install --batch transport-reactor-netty4
