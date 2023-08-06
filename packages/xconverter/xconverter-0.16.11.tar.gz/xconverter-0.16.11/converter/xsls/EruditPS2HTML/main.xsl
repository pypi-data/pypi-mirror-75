<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    xmlns:str="http://exslt.org/strings" xmlns:converter="converter"
    exclude-result-prefixes="converter xs str" version="2.0">

    <xsl:import href="utils.xsl"/>
    <xsl:param name="assets_path"/>
    <xsl:variable name="document_language" select="article/@xml:lang"/>

    <xsl:template match="article">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <html>
            <head>
                <title><xsl:value-of select="front/journal-meta/journal-title-group/journal-title"/>: <xsl:value-of select="front/article-meta/title-group/article-title"/></title>
                <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
                <meta name="journal-title">
                    <xsl:attribute name="content">
                        <xsl:apply-templates select="front/journal-meta/journal-title-group/journal-title"/><xsl:if test="front/journal-meta/journal-title-group/journal-subtitle"><xsl:value-of select="' : '"/><xsl:apply-templates select="front/journal-meta/journal-title-group/journal-subtitle"/></xsl:if>
                    </xsl:attribute>
                </meta>
                <meta name="issue-label">
                    <xsl:attribute name="content">
                        <xsl:if test="front/article-meta/issue-title"><xsl:apply-templates select="front/article-meta/issue-title"/><xsl:value-of select="', '"/></xsl:if><xsl:apply-templates select="front/article-meta/volume"/><xsl:apply-templates select="front/article-meta/issue"/><xsl:value-of select="' '"/><xsl:apply-templates select="front/article-meta/pub-date[@date-type='collection']/season"/><xsl:value-of select="' '"/><xsl:apply-templates select="front/article-meta/pub-date[@date-type='collection']/year"/>
                    </xsl:attribute>
                </meta>
                <meta name="license">
                    <xsl:attribute name="content">
                        <xsl:value-of select="front/article-meta/permissions/copyright-statement | front/article-meta/permissions/license/license-p"/>
                    </xsl:attribute>
                    <xsl:value-of select="front/article-meta/permissions/copyright-statement | front/article-meta/permissions/license/license-p"/>
                </meta>
                <meta name="doi">
                    <xsl:attribute name="content">https://doi.org/<xsl:value-of select="front/article-meta/article-id[@pub-id-type = 'doi']"/></xsl:attribute>
                </meta>
            </head>
            <body>
                <div class="document">
                    <div class="cover">
                        <div class="journal-title">
                            <xsl:apply-templates select="front/journal-meta/journal-title-group/journal-title"/><xsl:if test="front/journal-meta/journal-title-group/journal-subtitle"><xsl:value-of select="' : '"/><xsl:apply-templates select="front/journal-meta/journal-title-group/journal-subtitle"/></xsl:if>
                        </div>
                        <div class="issue-label">
                            <xsl:if test="front/article-meta/issue-title"><xsl:apply-templates select="front/article-meta/issue-title"/><xsl:value-of select="', '"/></xsl:if><xsl:apply-templates select="front/article-meta/volume"/><xsl:apply-templates select="front/article-meta/issue"/><xsl:value-of select="' '"/><xsl:apply-templates select="front/article-meta/pub-date[@date-type='collection']/season"/><xsl:value-of select="' '"/><xsl:apply-templates select="front/article-meta/pub-date[@date-type='collection']/year"/>
                        </div>
                        <div class="license">
                            <div class="statement">
                                <xsl:value-of select="front/article-meta/permissions/copyright-statement | front/article-meta/permissions/license/license-p"/>
                            </div>
                            <xsl:apply-templates select="front/article-meta/permissions/license"/>
                        </div>
                        <xsl:apply-templates select="front/article-meta/article-id[@pub-id-type = 'doi']" />
                    </div>
                    <div class="article">
                        <div class="front">
                            <div class="title-group">
                                <xsl:apply-templates select="front/article-meta/title-group/article-title"/>
                                <xsl:apply-templates select="front/article-meta/title-group/subtitle"/>
                                <xsl:apply-templates select="front/article-meta/product/related-object" mode="reviewed-product"/>
                            </div>
                            <xsl:apply-templates select="front/article-meta/title-group/trans-title-group"/>
                            <xsl:apply-templates select="front/article-meta/contrib-group"/>
                            <xsl:apply-templates select="front/notes" mode="editorial-notes"/>
                            <xsl:if test="front/article-meta/abstract or front/article-meta/trans-abstract">
                                <div class="abstract-group">
                                    <xsl:apply-templates select="front/article-meta/abstract"/>
                                    <xsl:apply-templates select="front/article-meta/trans-abstract"/>
                                </div>
                            </xsl:if>
                        </div>
                        <div class="body_back">
                            <xsl:apply-templates select="body"/>
                            <div class="back">
                                <xsl:if test="count(back//ack) > 0">
                                    <div class="ack-group">
                                        <xsl:apply-templates select="back//ack"/>
                                    </div>
                                </xsl:if>
                                <xsl:if test="count(//bio) > 0">
                                    <div class="bio-notes">
                                        <div class="title">
                                            <xsl:call-template name="translation">
                                                <xsl:with-param name="key">Biographic Notes</xsl:with-param>
                                                <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                                            </xsl:call-template>
                                        </div>
                                        <xsl:apply-templates select="//bio"/>
                                    </div>
                                </xsl:if>
                                <xsl:apply-templates select="back/fn-group"/>
                                <xsl:apply-templates select="back/ref-list"/>
                                <xsl:if test="count(back//notes[@notes-type='annex']) > 0">
                                    <div class="annexes">
                                        <div class="title">
                                            <xsl:call-template name="translation">
                                                <xsl:with-param name="key">Annexes</xsl:with-param>
                                                <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                                            </xsl:call-template>
                                        </div>
                                        <xsl:apply-templates select="back/notes[@notes-type='annex']"/>
                                    </div>
                                </xsl:if>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="notes" mode="editorial-notes">
        <div class="editorial-notes">
            <div class="title">
                <xsl:call-template name="translation">
                    <xsl:with-param name="key">Editorial Notes</xsl:with-param>
                    <xsl:with-param name="language"><xsl:value-of select="$document_language"/></xsl:with-param>
                </xsl:call-template>
            </div>
            <xsl:apply-templates select="sec" mode="editorial-notes"/>
        </div>
    </xsl:template>

    <xsl:template match="sec" mode="editorial-notes">
        <div class="note">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="license">
        <div class="creative-commons">
            <xsl:choose>
                <xsl:when test="@xlink:href != ''">
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="@xlink:href"/>
                        </xsl:attribute>
                        <img>
                            <xsl:attribute name="src">
                                <xsl:value-of select="license-p/graphic/@xlink:href"/>
                            </xsl:attribute>
                        </img>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <img>
                        <xsl:attribute name="src">
                            <xsl:value-of select="license-p/graphic/@xlink:href"/>
                        </xsl:attribute>
                    </img>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="trans-title-group">
        <div class="trans-title-group">
            <xsl:apply-templates select="trans-title"/>
            <xsl:apply-templates select="trans-subtitle"/>
        </div>
    </xsl:template>

    <xsl:template match="body">
        <div class="body">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="license-p">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="issue-title">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="issue">(<xsl:value-of select="."/>)</xsl:template>

    <xsl:template match="volume"><xsl:value-of select="."/></xsl:template>

    <xsl:template match="season"><xsl:value-of select="."/></xsl:template>

    <xsl:template match="year"><xsl:value-of select="."/></xsl:template>

    <xsl:template match="journal-title">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="journal-subtitle">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="notes">
        <div class="annex">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="bio">
        <div class="bio">
            <xsl:apply-templates select="p" />
        </div>
    </xsl:template>

    <xsl:template match="ack">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="ack">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">Acknowledgement</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="p" />
        </div>
    </xsl:template>

    <xsl:template match="article-title">
        <div class="article-title">
            <xsl:apply-templates select="."  mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="trans-title">
        <div class="trans-title">
            <xsl:apply-templates select="."  mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="subtitle">
        <div class="subtitle">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="trans-subtitle">
        <div class="trans-subtitle">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="related-object" mode="reviewed-product">
        <div class="reviewed-product">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="sec">
        <div class="sec">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote">
        <div class="disp-quote">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='dedication']">
        <div class="dedication">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='example']">
        <div class="example">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='block-citation']">
        <div class="block-citation">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='verbatim']">
        <div class="verbatim">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="disp-quote[@content-type='epigraph']">
        <div class="epigraph">
            <xsl:apply-templates select="*"/>
        </div>
    </xsl:template>

    <xsl:template match="attrib">
        <div class="attrib">
            <xsl:apply-templates select="." mode="text_with_formating" />
        </div>
    </xsl:template>

    <xsl:template match="sec/label"/>

    <xsl:template match="fn-group">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="footnotes">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">Notes</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="fn"/>
        </div>
    </xsl:template>

    <xsl:template match="ref-list">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="ref-list">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">References</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="p"/>
            <xsl:if test="ref">
                <ul>
                    <xsl:apply-templates select="ref"/>
                </ul>
            </xsl:if>
            <xsl:apply-templates select="ref-list" mode="sub-ref-list"/>
        </div>
    </xsl:template>

    <xsl:template match="ref-list" mode="sub-ref-list">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="ref-list-sec">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">References</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="p"/>
            <xsl:if test="ref">
                <ul>
                    <xsl:apply-templates select="ref"/>
                </ul>
            </xsl:if>
        </div>
    </xsl:template>

    <xsl:template match="fn">
        <div class="footnote">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:apply-templates select="label" mode="footnote"/>
            <xsl:apply-templates select="p"/>
        </div>
    </xsl:template>

    <xsl:template match="label" mode="footnote">
        <div class="label">
            [<a><xsl:attribute name="href">#rel<xsl:value-of select="../@id"/></xsl:attribute><xsl:value-of select="."/></a>]
        </div>
    </xsl:template>

    <xsl:template match="label">
        <div class="label">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="caption">
        <div class="caption">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="xref">
        <sup>
            <a href="#">
                <xsl:attribute name="href">#<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="id">rel<xsl:value-of select="@rid"/></xsl:attribute>
                <xsl:attribute name="class">xref</xsl:attribute>
                <xsl:value-of select="."/>
            </a>
        </sup>
    </xsl:template>

    <xsl:template match="ref">
        <li class="ref">
            <xsl:apply-templates select=" mixed-citation"/>
            <xsl:apply-templates select="element-citation/pub-id[@pub-id-type='doi']" mode="doi"/>
        </li>
    </xsl:template>

    <xsl:template match="mixed-citation">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="pub-id" mode="doi">
        <xsl:variable name="doi">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <div class="doi">doi : <a href="{$doi}"><xsl:value-of select="$doi"/></a></div>
    </xsl:template>

    <xsl:template match="abstract|trans-abstract">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="abstract">
            <xsl:if test="not(title) or title = ''">
                <div class="title">
                     <xsl:call-template name="translation">
                         <xsl:with-param name="key">Abstract</xsl:with-param>
                         <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                     </xsl:call-template>
                </div>
            </xsl:if>
            <xsl:apply-templates select="*"/>
            <xsl:apply-templates select="../kwd-group[@xml:lang = $lang]"/>
        </div>
    </xsl:template>

    <xsl:template match="kwd-group">
        <xsl:variable name="lang">
            <xsl:choose>
                <xsl:when test="@xml:lang != ''"><xsl:value-of select="@xml:lang"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="$document_language"/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="kwd-group">
            <xsl:choose>
                <xsl:when test="title != ''">
                    <xsl:apply-templates select="title"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="title">
                        <xsl:call-template name="translation">
                            <xsl:with-param name="key">Keywords</xsl:with-param>
                            <xsl:with-param name="language"><xsl:value-of select="$lang"/></xsl:with-param>
                        </xsl:call-template>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <ul>
                <xsl:apply-templates select="kwd"/>
            </ul>
        </div>
    </xsl:template>

    <xsl:template match="kwd">
        <li>
            <xsl:value-of select="."/>
        </li>
    </xsl:template>

    <xsl:template match="title">
        <div class="title">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='center']">
        <center>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </center>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-uppercase']">
        <span class="text-uppercase">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-boxed']">
        <span class="text-boxed">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-smaller']">
        <small>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </small>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-bigger']">
        <big>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </big>
    </xsl:template>

    <xsl:template match="styled-content[@style-type='text-uppercase']">
        <span class="text-uppercase">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="p">
        <p>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </p>
    </xsl:template>

    <xsl:template match="contrib-group">
        <div class="contrib-group">
            <xsl:apply-templates select="contrib"/>
        </div>
    </xsl:template>

    <xsl:template match="contrib">
        <div class="contrib">
            <div class="name">
                <xsl:value-of select="name/given-names"/>&#160;<span class="surname"><xsl:value-of select="name/surname"/></span>
            </div>
            <xsl:apply-templates select="string-name"/>
            <xsl:apply-templates select="xref" mode="affiliation"/>
            <xsl:apply-templates select="email"/>
        </div>
    </xsl:template>

    <xsl:template match="contrib[@contrib-type='group']">
        <xsl:apply-templates select="collab"/>
    </xsl:template>

    <xsl:template match="collab">
        <div class="contrib-collab">
            <xsl:apply-templates select="named-content"/>
            <xsl:apply-templates select="contrib-group/contrib"/>
        </div>
    </xsl:template>

    <xsl:template match="named-content[@content-type='name']">
        <div class="collab-name">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="string-name[@content-type='alias']">
        <div class="alias">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="email">
        <div class="email">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="xref" mode="affiliation">
        <xsl:variable name="aff_id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:apply-templates select="//aff[@id=$aff_id]/institution"/>
    </xsl:template>

    <xsl:template match="institution">
        <div class="institution">
            <xsl:value-of select="."/>
        </div>
    </xsl:template>

    <xsl:template match="article-id">
        <xsl:variable name="link">http://doi.org/<xsl:value-of select="."/></xsl:variable>
        <div class="article-id"><a href="{$link}"><xsl:value-of select="$link"/></a></div>
    </xsl:template>

    <xsl:template match="boxed-text">
        <div class="boxed-text">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="boxed-header">
                        <xsl:apply-templates select="label|caption"/>
                    </div>
                    <div class="boxed-content">
                        <xsl:apply-templates select="sec|p|disp-quote"/>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="boxed-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="attrib"/>
        </div>
    </xsl:template>

    <xsl:template match="caption">
        <div class="caption">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </div>
    </xsl:template>

    <xsl:template match="list[@list-type = 'simple']">
        <ul>
            <xsl:apply-templates select="*"/>
        </ul>
    </xsl:template>

    <xsl:template match="list[@list-type = 'order']">
        <ol>
            <xsl:apply-templates select="*"/>
        </ol>
    </xsl:template>

    <xsl:template match="list-item">
        <li><xsl:apply-templates select="." mode="text_with_formating" /></li>
    </xsl:template>

    <xsl:template match="italic">
        <i><xsl:apply-templates select="." mode="text_with_formating" /></i>
    </xsl:template>

    <xsl:template match="bold">
        <b><xsl:apply-templates select="." mode="text_with_formating" /></b>
    </xsl:template>

    <xsl:template match="sc">
        <small>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </small>
    </xsl:template>

    <xsl:template match="overline">
        <span class="text-overline">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="monospace">
        <span class="text-monospace">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="strike">
        <span class="text-strike">
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </span>
    </xsl:template>

    <xsl:template match="underline">
        <u>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </u>
    </xsl:template>

    <xsl:template match="sup">
        <sup>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sup>
    </xsl:template>

    <xsl:template match="sub">
        <sub>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </sub>
    </xsl:template>

    <xsl:template match="def-list">
        <table class="def-list">
            <xsl:if test="term-head or def-head">
                <tr>
                    <th class="term-head"><xsl:apply-templates select="term-head" mode="text_with_formating"/></th>
                    <th class="def-head"><xsl:apply-templates select="def-head" mode="text_with_formating"/></th>
                </tr>
            </xsl:if>
            <xsl:apply-templates select="def-item"/>
        </table>
    </xsl:template>

    <xsl:template match="def-item">
        <tr>
            <td class="term"><p><xsl:apply-templates select="term/*|term/text()"/></p></td>
            <td class="def"><xsl:apply-templates select="def/*"/></td>
        </tr>
    </xsl:template>

    <xsl:template match="disp-formula-group">
        <div class="disp-formula-group">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="disp-formula-group-header">
                        <xsl:apply-templates select="label|caption"/>
                    </div>
                    <div class="disp-formula-group-content">
                        <xsl:apply-templates select="disp-formula|disp-formula-group"/>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="disp-formula-group-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula">
        <div class="disp-formula">
            <xsl:apply-templates select="*|text()"/>
        </div>
    </xsl:template>

    <xsl:template match="fig-group">
        <div class="fig-group">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="fig-group-header">
                        <xsl:apply-templates select="label|caption"/>
                    </div>
                    <div class="fig-group-content">
                        <xsl:apply-templates select="fig|graphic|media"/>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="fig-group-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="fig">
        <div class="fig">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="fig-header">
                        <xsl:apply-templates select="label|caption/title"/>
                    </div>
                    <div class="fig-content">
                        <xsl:apply-templates select="graphic|media"/>
                    </div>
                    <xsl:apply-templates select="caption/p" mode="fig-caption-notes"/>
                    <xsl:apply-templates select="attrib"/>
                    <xsl:apply-templates select="permissions"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="fig-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="p" mode="fig-caption-notes">
        <div class="figure-notes">
            <xsl:apply-templates select="." />
        </div>
    </xsl:template>

    <xsl:template match="p" mode="figure-caption-notes">
        <div class="caption-note">
            <div class="content"><xsl:apply-templates select="p" /></div>
        </div>
    </xsl:template>

    <xsl:template match="ext-link">
        <xsl:choose>
            <xsl:when test="(. != '') and (. != @xlink:href)">
                <xsl:value-of select="."/> (<a><xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute><xsl:value-of select="@xlink:href"/></a>)
            </xsl:when>
            <xsl:otherwise>
                (<a><xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute><xsl:value-of select="@xlink:href"/></a>)
            </xsl:otherwise>
        </xsl:choose>
</xsl:template>

    <xsl:template match="inline-graphic">
        <span class="inline-graphic">
            <img>
                <xsl:attribute name="src"><xsl:if test="$assets_path != ''"><xsl:value-of select="$assets_path"/>/</xsl:if><xsl:value-of select="@xlink:href"/></xsl:attribute>
            </img>
        </span>
    </xsl:template>

    <xsl:template match="inline-formula">
        <xsl:apply-templates select="." mode="text_with_formating"/>
    </xsl:template>

    <xsl:template match="graphic">
        <div>
            <xsl:attribute name="class">image-<xsl:value-of select="@position"/></xsl:attribute>
            <img>
                <xsl:attribute name="src"><xsl:if test="$assets_path != ''"><xsl:value-of select="$assets_path"/>/</xsl:if><xsl:value-of select="@xlink:href"/></xsl:attribute>
            </img>
        </div>
    </xsl:template>

    <xsl:template match="media[@mimetype='audio']">
        <xsl:variable name="article-id" select="/article/front/article-meta/article-id[@pub-id-type='publisher-id']/text()"/>
        <xsl:variable name="journal-id" select="/article/front/journal-meta/journal-title-group/abbrev-journal-title/text()"/>
        <xsl:variable name="media_url" select="concat('http://www.erudit.org/media/',$journal-id,'/',$article-id,'/', @xlink:href)"/>
        <xsl:variable name="article_url" select="concat('http://id.erudit.org/iderudit/',$article-id)"/>
        <div class="media-audio-group">
            <div class="media-audio-group-caption">
                <xsl:apply-templates select="label|caption"/>
            </div>
            <div class="media_print_note">media disponible au: <a href="{$article_url}"><xsl:value-of select="$article_url"/></a></div>
        </div>
    </xsl:template>

    <xsl:template match="media[@mimetype='video']">
        <xsl:variable name="article-id" select="/article/front/article-meta/article-id[@pub-id-type='publisher-id']/text()"/>
        <xsl:variable name="journal-id" select="/article/front/journal-meta/journal-title-group/abbrev-journal-title/text()"/>
        <xsl:variable name="media_url" select="concat('http://www.erudit.org/media/',$journal-id,'/',$article-id,'/', @xlink:href)"/>
        <xsl:variable name="article_url" select="concat('http://id.erudit.org/iderudit/',$article-id)"/>
        <div class="media-video-group">
            <div class="media-video-group-caption">
                <xsl:apply-templates select="label|caption"/>
            </div>
            <div class="media_print_note">media disponible au: <a href="{$article_url}"><xsl:value-of select="$article_url"/></a></div>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap-group">
        <div class="table-wrap-group">
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="table-wrap-group-header">
                        <xsl:apply-templates select="label|caption"/>
                    </div>
                    <div class="table-wrap-group-content">
                        <xsl:apply-templates select="table-wrap"/>
                    </div>
                </xsl:when>
                <xsl:otherwise>
                    <div class="table-wrap-group-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap">
        <div class="table-wrap">
            <xsl:attribute name="id"><xsl:value-of select="@id"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="label|caption">
                    <div class="table-wrap-header">
                        <xsl:apply-templates select="label|caption/title"/>
                    </div>
                    <div class="table-wrap-content">
                        <xsl:apply-templates select="media|graphic|table"/>
                    </div>
                    <xsl:apply-templates select="table-wrap-foot"/>
                    <xsl:apply-templates select="permissions"/>
                </xsl:when>
                <xsl:otherwise>
                    <div class="table-wrap-content">
                        <xsl:apply-templates select="*"/>
                    </div>
                </xsl:otherwise>
            </xsl:choose>

        </div>
    </xsl:template>

    <xsl:template match="table-wrap-foot">
        <xsl:if test="fn-group/fn or ../caption/p">
            <div class="table-notes">
                <xsl:apply-templates select="../caption/p" mode="table-caption-notes"/>
                <xsl:apply-templates select="fn-group/fn" mode="table-notes"/>
            </div>
        </xsl:if>
        <xsl:apply-templates select="attrib"/>
    </xsl:template>

    <xsl:template match="p" mode="table-caption-notes">
        <div class="caption-note">
            <div class="content"><xsl:apply-templates select="." /></div>
        </div>
    </xsl:template>

    <xsl:template match="fn" mode="table-notes">
        <div class="note">
            <xsl:apply-templates select="label" />
            <div class="content"><xsl:apply-templates select="p" /></div>
        </div>
    </xsl:template>

    <xsl:template match="table">
        <table>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </table>
    </xsl:template>

    <xsl:template match="colgroup">
        <colgroup>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </colgroup>
    </xsl:template>

    <xsl:template match="col">
        <col>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </col>
    </xsl:template>


    <xsl:template match="tr">
        <tr>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tr>
    </xsl:template>

    <xsl:template match="td">
        <td>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </td>
    </xsl:template>

    <xsl:template match="th">
        <th>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </th>
    </xsl:template>

    <xsl:template match="thead">
        <thread>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </thread>
    </xsl:template>

    <xsl:template match="tfoot">
        <tfoot>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tfoot>
    </xsl:template>

    <xsl:template match="tbody">
        <tbody>
            <xsl:apply-templates select="@*" mode="table-attr"/>
            <xsl:apply-templates select="." mode="text_with_formating"/>
        </tbody>
    </xsl:template>

    <xsl:template match="@*" mode="table-attr">
        <xsl:attribute name="{name()}">
            <xsl:value-of select="."/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="mml:math">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates mode="mathml"/>
        </math>
    </xsl:template>

    <xsl:template match="*" mode="mathml">
        <xsl:element name="{local-name()}" xmlns="http://www.w3.org/1998/Math/MathML">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates mode="mathml"/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="* | text()" mode="text_with_formating">
        <xsl:apply-templates select="* | text()"/>
    </xsl:template>

    <xsl:template match="*">
        <PENDING-TREATMENT>
            <xsl:copy-of select="."/>
        </PENDING-TREATMENT>
    </xsl:template>

</xsl:stylesheet>