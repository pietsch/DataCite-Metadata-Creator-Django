<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:d="http://datacite.org/schema/kernel-2.2"
    exclude-result-prefixes="d"
>
  <xsl:output method="html"/>
  <xsl:include href="custom_style.xsl"/>

  <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyzäöü'" />
  <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'" />
  <xsl:variable name="my_base_url" select="'http://sfb882.uni-bielefeld.de/publications/data/doi/'" />
  <xsl:variable name="pevz_resolver">http://ekvv.uni-bielefeld.de/pers_publ/publ/PersonDetail.jsp?personId=</xsl:variable>
  <xsl:variable name="doi_resolver">http://dx.doi.org/</xsl:variable>
  <xsl:variable name="viaf_resolver">http://viaf.org/viaf/</xsl:variable>
  <xsl:variable name="isni_resolver">http://isni.oclc.nl/DB=1.2/SET=4/TTL=18/CMD?ACT=SRCHA&amp;IKT=8006&amp;SRT=&amp;TRM=</xsl:variable>
  <xsl:variable name="orcid_resolver">http://orcid.org/</xsl:variable>
  <xsl:variable name="authorclaim_resolver">http://authorclaim.org/profile/</xsl:variable>
  <xsl:variable name="researcherid_resolver">http://www.researcherid.com/rid/</xsl:variable>

  <xsl:template name="add-line-breaks">
    <xsl:param name="string" select="." />
    <xsl:choose>
      <xsl:when test="contains($string, '&#xA;&#xA;')">
	<p> 
	<xsl:value-of select="substring-before($string, '&#xA;&#xA;')" />
	</p>
	<xsl:call-template name="add-line-breaks">
	  <xsl:with-param name="string"
			  select="substring-after($string, '&#xA;&#xA;')" />
	</xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="$string" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="person-link">
    <xsl:param name="text" select="." />
      <xsl:choose>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'RESEARCHERID'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($researcherid_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'AUTHORCLAIM'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($authorclaim_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'ORCID'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($orcid_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'ISNI'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($isni_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'VIAF'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($viaf_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'PERSONIDUNIBI'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($pevz_resolver,d:nameIdentifier)" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(d:nameIdentifier/@nameIdentifierScheme, $lowercase, $uppercase) = 'URL'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="d:nameIdentifier" /></xsl:attribute>
	    <xsl:value-of select="$text" />
	  </xsl:element>
	</xsl:when>
	<xsl:otherwise>
	    <xsl:value-of select="$text" />
	</xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <xsl:template name="citation">
    <dt>Suggested citation:</dt>
    <dd>
      <xsl:for-each select="d:resource/d:creators/d:creator"><xsl:value-of select="d:creatorName" /><xsl:if test="not(position() = last())">; </xsl:if></xsl:for-each>
      (<xsl:value-of select="d:resource/d:publicationYear"/>):
      <xsl:for-each select="d:resource/d:titles/d:title"><xsl:value-of select="."/>. </xsl:for-each>
      <xsl:value-of select="d:resource/d:publisher"/>.
      <xsl:element name="a">
	<xsl:attribute name="href"><xsl:value-of select="concat($doi_resolver, d:resource/d:identifier)" /></xsl:attribute>
	doi:<xsl:value-of select="d:resource/d:identifier" />
      </xsl:element>
    </dd>
  </xsl:template>



  <xsl:template match="/">
    <xsl:call-template name="custom-style" />
  </xsl:template>

  <xsl:template match="d:identifier" />

  <xsl:template match="d:creators">
    <dt>Creators:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:creators/d:creator">
    <dd>
      <xsl:call-template name="person-link">
	<xsl:with-param name="text" select="d:creatorName"/>
      </xsl:call-template>  
    </dd>
  </xsl:template>


  <xsl:template match="d:titles">
    <dt>Title:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:title">
    <dd><xsl:if test="@titleType"><xsl:value-of select="@titleType" />: </xsl:if> <b><xsl:value-of select="." /></b></dd>
  </xsl:template>

  <xsl:template match="d:publisher">
    <dt>Publisher:</dt>
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:publicationYear">
    <dt>Year of publication:</dt>
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:subjects">
    <dt>Subjects:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:subjects/d:subject">
    <dd><xsl:if test="@subjectScheme"><xsl:value-of select="@subjectScheme" />: </xsl:if><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:contributors">
    <dt>Contributors:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:contributors/d:contributor">
    <dd>
      <xsl:if test="@contributorType"><xsl:value-of select="@contributorType" />: </xsl:if>
      <xsl:call-template name="person-link">
	<xsl:with-param name="text" select="d:contributorName"/>
      </xsl:call-template>
    </dd>
  </xsl:template>

  <xsl:template match="d:dates">
    <dt>Dates:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:dates/d:date">
    <dd><xsl:if test="@dateType"><xsl:value-of select="@dateType" />: </xsl:if><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:language">
    <dt>Primary language of this resource (ISO 639):</dt>
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:resourceType">
    <dt>Resource type:</dt>
    <dd><xsl:value-of select="@resourceTypeGeneral" /><xsl:if test=". != ''"> (<xsl:value-of select="." />)</xsl:if></dd>
  </xsl:template>

  <xsl:template match="d:formats">
    <dt>Formats:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:formats/d:format">
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:alternateIdentifiers">
    <dt>Alternate identifiers:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:alternateIdentifiers/d:alternateIdentifier">
    <!-- TODO: if @alternateIdentifierType=="pubId" then hotlink it -->
    <dd><xsl:value-of select="@alternateIdentifierType" />: <xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:relatedIdentifiers">
    <dt>Related identifiers:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:relatedIdentifiers/d:relatedIdentifier">
    <dd>
      <xsl:value-of select="@relationType" />: <xsl:value-of select="@relatedIdentifierType" /><xsl:text> </xsl:text>
      <xsl:choose>
	<xsl:when test="translate(@relatedIdentifierType, $lowercase, $uppercase) = 'URL'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="." /></xsl:attribute>
	    <xsl:value-of select="." />
	  </xsl:element>
	</xsl:when>
	<xsl:when test="translate(@relatedIdentifierType, $lowercase, $uppercase) = 'DOI'">
	  <xsl:element name="a">
	    <xsl:attribute name="href"><xsl:value-of select="concat($doi_resolver, .)" /></xsl:attribute>
	    <xsl:value-of select="." />
	  </xsl:element>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:value-of select="." />
	</xsl:otherwise>
      </xsl:choose>
    </dd>
  </xsl:template>

  <xsl:template match="d:sizes">
    <dt>Size:</dt>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:sizes/d:size">
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:version">
    <dt>Version:</dt>
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:rights">
    <dt>Rights (license):</dt>
    <dd><xsl:value-of select="." /></dd>
  </xsl:template>

  <xsl:template match="d:descriptions">
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="d:descriptions/d:description">
    <dt><xsl:value-of select="@descriptionType" />:</dt>
    <dd>
      <xsl:call-template name="add-line-breaks">
	<xsl:with-param name="text" select="."/>
      </xsl:call-template>  
    </dd>
  </xsl:template>

</xsl:stylesheet>
