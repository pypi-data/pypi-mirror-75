/* global discordPingformatterSettings */

jQuery(document).ready(function($) {
    /* Functions
    ----------------------------------------------------------------------------------------------------------------- */

    /**
     * convert line breaks into <br>
     *
     * @param {string} string
     * @param {bool} isXhtml
     */
    var nl2br = (function(string, isXhtml) {
        var breakTag = (isXhtml || typeof isXhtml === 'undefined') ? '<br />' : '<br>';

        return (string + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    });

    /**
     * closing the message
     *
     * @param {string} element
     * @returns {void}
     */
    var closeCopyMessageElement = (function(element) {
        /**
         * close after 10 seconds
         */
        $(element).fadeTo(10000, 500).slideUp(500, function() {
            $(this).slideUp(500, function() {
                $(this).remove();
            });
        });
    });

    /**
     * show message when copy action was successful
     *
     * @param {string} message
     * @param {string} element
     * @returns {undefined}
     */
    var showSuccess = (function(message, element) {
        $(element).html('<div class="alert alert-success alert-dismissable alert-copy-success"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message + '</div>');

        closeCopyMessageElement('.alert-copy-success');

        return;
    });

    /**
     * show message when copy action was not successful
     *
     * @param {string} message
     * @param {string} element
     * @returns {undefined}
     */
    var showError = (function(message, element) {
        $(element).html('<div class="alert alert-danger alert-dismissable alert-copy-error"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message + '</div>');

        closeCopyMessageElement('.alert-copy-error');

        return;
    });

    /**
     * sanitize input string
     *
     * @param {string} element
     * @returns {undefined}
     */
    var sanitizeInput = (function(input) {
        if(input) {
            return input.replace(/<(|\/|[^>\/bi]|\/[^>bi]|[^\/>][^>]+|\/[^>][^>]+)>/g, '');
        } else {
            return input;
        }
    });

    /**
     * send an embedded message to a Discord webhook
     *
     * @param {string} discordWebhook
     * @param {string} content
     * @param {array} embeds
     */
    var sendEmbeddedDiscordPing = (function(discordWebhook, content, embeds) {
        var request = new XMLHttpRequest();

        request.open('POST', discordWebhook);
        request.setRequestHeader('Content-type', 'application/json');

        var params = {
            username: '',
            avatar_url: '',
            content: content,
            embeds: [embeds]
        };

        request.send(JSON.stringify(params));
    });

    /**
     * send a message to a Discord webhook
     *
     * @param {string} discordWebhook
     * @param {string} discordPingText
     */
    var sendDiscordPing = (function(discordWebhook, discordPingText) {
        var request = new XMLHttpRequest();

        request.open('POST', discordWebhook);
        request.setRequestHeader('Content-type', 'application/json');

        var params = {
            username: '',
            avatar_url: '',
            content: discordPingText
        };

        request.send(JSON.stringify(params));
    });

    /**
     * convert hex color code in something Discord can handle
     *
     * @param {string} hexValue
     */
    var hexToDecimal = (function(hexValue) {
        return parseInt(hexValue.replace('#',''), 16);
    });

    /**
     * convert the datepicker info into an URL that the
     * aa-tomezones module understands
     *
     * @param {string} formupTime
     */
    var getTimezonesUrl = (function(formupTime) {
        var formupTimestamp = ((new Date(formupTime + ' UTC')).getTime()) / 1000;
        var timezonesUrl = discordPingformatterSettings.siteUrl + 'timezones/?#' + formupTimestamp;

        return timezonesUrl;
    });

    /**
     * create the ping text
     */
    var generateDiscordPing = (function() {
        var pingTarget = sanitizeInput($('select#pingTarget option:selected').val());
        var pingTargetText = sanitizeInput($('select#pingTarget option:selected').text());
        var fleetType = sanitizeInput($('select#fleetType option:selected').val());
        var webhookEmbedColor = sanitizeInput($('select#fleetType option:selected').data('embed-color'));
        var fcName = sanitizeInput($('input#fcName').val());
        var fleetName = sanitizeInput($('input#fleetName').val());
        var formupLocation = sanitizeInput($('input#formupLocation').val());
        var formupTime = sanitizeInput($('input#formupTime').val());
        var fleetComms = sanitizeInput($('input#fleetComms').val());
        var fleetDoctrine = sanitizeInput($('input#fleetDoctrine').val());
        var fleetSrp = sanitizeInput($('select#fleetSrp option:selected').val());
        var additionalInformation = sanitizeInput($('textarea#additionalInformation').val());

        // ping webhooks, if configured
        var discordWebhook = false;

        if($('select#pingChannel').length) {
            discordWebhook = sanitizeInput($('select#pingChannel option:selected').val());
        }

        $('.aa-discord-ping-formatter-ping').show();

        var discordWebhookPingTextHeader = '';
        var discordWebhookPingTextContent = '';
        var discordWebhookPingTextFooter = '';
        var discordPingText = '';

        // determine pingTargetText
        if(pingTargetText.indexOf('@') > -1) {
            discordPingTarget = pingTargetText;
        } else {
            discordPingTarget = '@' + pingTargetText;
        }

        // determine pingTarget
        if(pingTarget.indexOf('@') > -1) {
            webhookPingTarget = pingTarget;
        } else {
            webhookPingTarget = '<@&' + pingTarget + '>';
        }

        // separator
        discordPingText += ' :: ';

        // fleet announcement
        discordPingText += '**';

        // check if it's a pre-ping or not
        if($('input#prePing').is(':checked')) {
            discordPingText += '### PRE PING ###';
            discordWebhookPingTextHeader += '### PRE PING ###';

            if(fleetType !== '') {
                discordPingText += ' / ' + fleetType + ' Fleet';
                discordWebhookPingTextHeader += ' / ' + fleetType + ' Fleet';
            }
        } else {
            if(fleetType !== '') {
                discordPingText += fleetType + ' ';
                discordWebhookPingTextHeader += fleetType + ' ';
            }

            discordPingText += 'Fleet is up';
            discordWebhookPingTextHeader += 'Fleet is up';
        }

        discordPingText += '**' + "\n";

        // check if FC name is available
        if(fcName !== '') {
            discordPingText += "\n" + '**FC:** ' + fcName;
            discordWebhookPingTextContent += "\n" + '**FC:** ' + fcName;
        }

        // check if fleet name is available
        if(fleetName !== '') {
            discordPingText += "\n" + '**Fleet Name:** ' + fleetName;
            discordWebhookPingTextContent += "\n" + '**Fleet Name:** ' + fleetName;
        }

        // check if form-up location is available
        if(formupLocation !== '') {
            discordPingText += "\n" + '**Formup Location:** ' + formupLocation;
            discordWebhookPingTextContent += "\n" + '**Formup Location:** ' + formupLocation;
        }

        // check if form-up time is available
        if($('input#formupTimeNow').is(':checked')) {
            discordPingText += "\n" + '**Formup Time:** NOW';
            discordWebhookPingTextContent += "\n" + '**Formup Time:** NOW';
        } else {
            if(formupTime !== '') {
                discordPingText += "\n" + '**Formup Time:** ' + formupTime;
                discordWebhookPingTextContent += "\n" + '**Formup Time:** ' + formupTime;

                // get the timestamp and build the link to the timezones module if it's installed
                if(discordPingformatterSettings.timezonesInstalled === true) {
                    var timezonesUrl = getTimezonesUrl(formupTime);

                    discordPingText += ' - ' + timezonesUrl;
                    discordWebhookPingTextContent += ' ([Time Zone Conversion](' + timezonesUrl + '))';
                }
            }
        }

        // check if fleet comms is available
        if(fleetComms !== '') {
            discordPingText += "\n" + '**Comms:** ' + fleetComms;
            discordWebhookPingTextContent += "\n" + '**Comms:** ' + fleetComms;
        }

        // check if doctrine is available
        if(fleetDoctrine !== '') {
            discordPingText += "\n" + '**Ships / Doctrine:** ' + fleetDoctrine;
            discordWebhookPingTextContent += "\n" + '**Ships / Doctrine:** ' + fleetDoctrine;
        }

        // check if srp is available
        if(fleetSrp !== '') {
            discordPingText += "\n" + '**SRP:** ' + fleetSrp;
            discordWebhookPingTextContent += "\n" + '**SRP:** ' + fleetSrp;
        }

        // check if additional information is available
        if(additionalInformation !== '') {
            discordPingText += "\n\n" + '**Additional Information**:' + "\n" + additionalInformation;
            discordWebhookPingTextContent += "\n\n" + '**Additional Information**:' + "\n" + additionalInformation;
        }

        $('.aa-discord-ping-formatter-ping-text').html('<p>' + nl2br(discordPingTarget + discordPingText) + '</p>');

        // ping it directly if a webhook is selected
        if(discordWebhook !== false && discordWebhook !== '') {
            // add ping creator at the end
            if(discordPingformatterSettings.pingCreator !== '') {
                discordPingText += "\n\n" + '*(Ping sent by: ' + discordPingformatterSettings.pingCreator + ')*';
                discordWebhookPingTextFooter = '(Ping sent by: ' + discordPingformatterSettings.pingCreator + ')';
            }

            // send the ping
            if(discordPingformatterSettings.embedPing === true) {
                var embedColor = '#FAA61A';

                if(fleetType !== '' && embedColor !== '') {
                    embedColor = webhookEmbedColor;
                }

                sendEmbeddedDiscordPing(
                    discordWebhook,
                    webhookPingTarget + ' :: **' + discordWebhookPingTextHeader + ' under ' + fcName + '**' + "\n" + '** **',
                    // embedded content » https://discohook.org/ - https://leovoel.github.io/embed-visualizer/
                    {
                        'title': '**Fleet Details**',
                        'description': discordWebhookPingTextContent,
                        'color': hexToDecimal(embedColor),
                        'footer': {
                            'text': discordWebhookPingTextFooter
                        }
                    }
                );
            } else {
                sendDiscordPing(discordWebhook, webhookPingTarget + discordPingText);
            }

            // tell the FC that it's already pinged
            showSuccess(
                'Success, your ping has been sent to your Discord.',
                '.aa-discord-ping-formatter-ping-copyresult'
            );
        }
    });

    /**
     * copy the discord ping to clipboard
     */
    var copyDiscordPing = (function() {
        /**
         * copy text to clipboard
         *
         * @type Clipboard
         */
        var clipboardDiscordPingData = new Clipboard('button#copyDiscordPing');

        /**
         * copy success
         *
         * @param {type} e
         */
        clipboardDiscordPingData.on('success', function(e) {
            showSuccess(
                'Success, Ping copied to clipboard. Now be a good FC and throw it in your Discord so you actually get some people in fleet.',
                '.aa-discord-ping-formatter-ping-copyresult'
            );

            e.clearSelection();
            clipboardDiscordPingData.destroy();
        });

        /**
         * copy error
         */
        clipboardDiscordPingData.on('error', function() {
            showError(
                'Error, Ping not copied to clipboard.',
                '.aa-discord-ping-formatter-ping-copyresult'
            );

            clipboardDiscordPingData.destroy();
        });
    });

    /* Events
    ----------------------------------------------------------------------------------------------------------------- */

    /**
     * toggle "Formup NOW" checkbox when "Pre-Ping" is toggled
     *
     * Behaviour:
     *  Pre-Ping checked » Formup NOW unchecked and disabled
     *  Pre-Ping unchecked » Formup NOW checked and enabled
     */
    $('#prePing').on('change', function() {
        if($('input#prePing').is(':checked')) {
            $('#formupTimeNow').removeAttr('checked');
            $('#formupTimeNow').prop('disabled', true);
            $('#formupTime').removeAttr('disabled');
        } else {
            $('#formupTimeNow').prop('checked', true);
            $('#formupTimeNow').removeAttr('disabled');
            $('#formupTime').prop('disabled', true);
        }
    });

    $('#formupTimeNow').on('change', function() {
        if($('input#formupTimeNow').is(':checked')) {
            $('#formupTime').prop('disabled', true);
        } else {
            $('#formupTime').removeAttr('disabled');
        }
    });

    /**
     * generate ping text
     */
    $('button#createPingText').on('click', function() {
        generateDiscordPing();
    });

    /**
     * copy ping text
     */
    $('button#copyDiscordPing').on('click', function() {
        copyDiscordPing();
    });
});
