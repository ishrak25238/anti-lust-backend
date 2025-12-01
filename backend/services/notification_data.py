
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class Template:
    subject: str
    body_html: str
    body_text: str
    sms_text: str
    push_title: str
    push_body: str

class NotificationTemplates:
    """
    Massive repository of multi-language notification templates.
    Supports 12 languages: English, Spanish, French, German, Italian, Portuguese,
    Russian, Japanese, Chinese, Korean, Arabic, Hindi.
    """
    
    def __init__(self):
        self.templates: Dict[str, Dict[str, Template]] = {
            'en': {
                'threat_blocked': Template(
                    subject="🚨 THREAT BLOCKED: Suspicious Activity Detected",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ THREAT PREVENTED</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Attention Parent/Guardian,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    The Anti-Lust Guardian system has successfully intercepted and blocked a potential threat on the monitored device.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Incident Details:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Type:</strong> {event_type}</li>
                                        <li><strong>Device:</strong> {device_id}</li>
                                        <li><strong>Time:</strong> {timestamp}</li>
                                        <li><strong>Confidence:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    No action is required. The content was not displayed to the user.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">View Full Report</a>
                                </div>
                            </div>
                            <div style="background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #999999;">
                                &copy; 2024 Anti-Lust Guardian. Automated Defense System.
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="THREAT BLOCKED\n\nAnti-Lust Guardian has blocked a threat on device {device_id}.\nType: {event_type}\nTime: {timestamp}\n\nNo action required.",
                    sms_text="🚨 Anti-Lust Alert: Threat blocked on {device_id}. Type: {event_type}. View app for details.",
                    push_title="🛡️ Threat Blocked",
                    push_body="Suspicious content was intercepted on {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Time Limit Reached",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ TIME LIMIT REACHED</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Usage Alert,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    The daily time limit for <strong>{category}</strong> has been reached on device <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Usage Stats:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Category:</strong> {category}</li>
                                        <li><strong>Limit:</strong> {limit} minutes</li>
                                        <li><strong>Status:</strong> Locked</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Manage Limits</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="TIME LIMIT REACHED\n\nDevice {device_id} has reached the limit for {category}.\nAccess is now restricted.",
                    sms_text="⏳ Time Limit: {device_id} reached {limit}m limit for {category}. Access locked.",
                    push_title="⏳ Time's Up",
                    push_body="{device_id} reached the limit for {category}."
                )
            },
            'es': {
                'threat_blocked': Template(
                    subject="🚨 AMENAZA BLOQUEADA: Actividad Sospechosa Detectada",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ AMENAZA PREVENIDA</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Atención Padre/Tutor,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    El sistema Anti-Lust Guardian ha interceptado y bloqueado exitosamente una amenaza potencial en el dispositivo monitoreado.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Detalles del Incidente:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Tipo:</strong> {event_type}</li>
                                        <li><strong>Dispositivo:</strong> {device_id}</li>
                                        <li><strong>Hora:</strong> {timestamp}</li>
                                        <li><strong>Confianza:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    No se requiere acción. El contenido no fue mostrado al usuario.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Ver Informe Completo</a>
                                </div>
                            </div>
                            <div style="background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #999999;">
                                &copy; 2024 Anti-Lust Guardian. Sistema de Defensa Automatizado.
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="AMENAZA BLOQUEADA\n\nAnti-Lust Guardian ha bloqueado una amenaza en el dispositivo {device_id}.\nTipo: {event_type}\nHora: {timestamp}\n\nNo se requiere acción.",
                    sms_text="🚨 Alerta Anti-Lust: Amenaza bloqueada en {device_id}. Tipo: {event_type}. Ver app para detalles.",
                    push_title="🛡️ Amenaza Bloqueada",
                    push_body="Se interceptó contenido sospechoso en {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Límite de Tiempo Alcanzado",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ LÍMITE ALCANZADO</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Alerta de Uso,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    El límite de tiempo diario para <strong>{category}</strong> se ha alcanzado en el dispositivo <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Estadísticas de Uso:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Categoría:</strong> {category}</li>
                                        <li><strong>Límite:</strong> {limit} minutos</li>
                                        <li><strong>Estado:</strong> Bloqueado</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Gestionar Límites</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="LÍMITE ALCANZADO\n\nEl dispositivo {device_id} ha alcanzado el límite para {category}.\nEl acceso está restringido.",
                    sms_text="⏳ Límite: {device_id} alcanzó el límite de {limit}m para {category}. Acceso bloqueado.",
                    push_title="⏳ Tiempo Agotado",
                    push_body="{device_id} alcanzó el límite para {category}."
                )
            },
            'fr': {
                'threat_blocked': Template(
                    subject="🚨 MENACE BLOQUÉE : Activité Suspecte Détectée",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ MENACE ÉVITÉE</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Attention Parent/Tuteur,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Le système Anti-Lust Guardian a intercepté et bloqué avec succès une menace potentielle sur l'appareil surveillé.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Détails de l'incident :</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Type :</strong> {event_type}</li>
                                        <li><strong>Appareil :</strong> {device_id}</li>
                                        <li><strong>Heure :</strong> {timestamp}</li>
                                        <li><strong>Confiance :</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    Aucune action requise. Le contenu n'a pas été affiché à l'utilisateur.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Voir le rapport complet</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="MENACE BLOQUÉE\n\nAnti-Lust Guardian a bloqué une menace sur l'appareil {device_id}.\nType : {event_type}\nHeure : {timestamp}\n\nAucune action requise.",
                    sms_text="🚨 Alerte Anti-Lust : Menace bloquée sur {device_id}. Type : {event_type}. Voir l'appli pour les détails.",
                    push_title="🛡️ Menace Bloquée",
                    push_body="Contenu suspect intercepté sur {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Limite de Temps Atteinte",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ LIMITE ATTEINTE</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Alerte d'utilisation,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    La limite de temps quotidienne pour <strong>{category}</strong> a été atteinte sur l'appareil <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Statistiques d'utilisation :</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Catégorie :</strong> {category}</li>
                                        <li><strong>Limite :</strong> {limit} minutes</li>
                                        <li><strong>Statut :</strong> Verrouillé</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Gérer les limites</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="LIMITE ATTEINTE\n\nL'appareil {device_id} a atteint la limite pour {category}.\nL'accès est restreint.",
                    sms_text="⏳ Limite : {device_id} a atteint la limite de {limit}m pour {category}. Accès verrouillé.",
                    push_title="⏳ Temps Écoulé",
                    push_body="{device_id} a atteint la limite pour {category}."
                )
            },
            'de': {
                'threat_blocked': Template(
                    subject="🚨 BEDROHUNG BLOCKIERT: Verdächtige Aktivität erkannt",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ BEDROHUNG VERHINDERT</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Achtung Eltern/Erziehungsberechtigte,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Das Anti-Lust Guardian System hat erfolgreich eine potenzielle Bedrohung auf dem überwachten Gerät abgefangen und blockiert.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Vorfall-Details:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Typ:</strong> {event_type}</li>
                                        <li><strong>Gerät:</strong> {device_id}</li>
                                        <li><strong>Zeit:</strong> {timestamp}</li>
                                        <li><strong>Konfidenz:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    Keine Handlung erforderlich. Der Inhalt wurde dem Benutzer nicht angezeigt.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Vollständigen Bericht ansehen</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="BEDROHUNG BLOCKIERT\n\nAnti-Lust Guardian hat eine Bedrohung auf Gerät {device_id} blockiert.\nTyp: {event_type}\nZeit: {timestamp}\n\nKeine Handlung erforderlich.",
                    sms_text="🚨 Anti-Lust Alarm: Bedrohung auf {device_id} blockiert. Typ: {event_type}. Details in der App.",
                    push_title="🛡️ Bedrohung Blockiert",
                    push_body="Verdächtiger Inhalt auf {device_id} abgefangen."
                ),
                'time_limit': Template(
                    subject="⏳ Zeitlimit Erreicht",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ ZEITLIMIT ERREICHT</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Nutzungsalarm,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Das tägliche Zeitlimit für <strong>{category}</strong> wurde auf Gerät <strong>{device_id}</strong> erreicht.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Nutzungsstatistiken:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Kategorie:</strong> {category}</li>
                                        <li><strong>Limit:</strong> {limit} Minuten</li>
                                        <li><strong>Status:</strong> Gesperrt</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Limits verwalten</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="ZEITLIMIT ERREICHT\n\nGerät {device_id} hat das Limit für {category} erreicht.\nZugriff ist eingeschränkt.",
                    sms_text="⏳ Limit: {device_id} hat {limit}m Limit für {category} erreicht. Zugriff gesperrt.",
                    push_title="⏳ Zeit Abgelaufen",
                    push_body="{device_id} hat das Limit für {category} erreicht."
                )
            },
            'ru': {
                'threat_blocked': Template(
                    subject="🚨 УГРОЗА ЗАБЛОКИРОВАНА: Обнаружена подозрительная активность",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ УГРОЗА ПРЕДОТВРАЩЕНА</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Внимание Родитель/Опекун,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Система Anti-Lust Guardian успешно перехватила и заблокировала потенциальную угрозу на отслеживаемом устройстве.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Детали инцидента:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Тип:</strong> {event_type}</li>
                                        <li><strong>Устройство:</strong> {device_id}</li>
                                        <li><strong>Время:</strong> {timestamp}</li>
                                        <li><strong>Доверие:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    Действий не требуется. Контент не был показан пользователю.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Посмотреть полный отчет</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="УГРОЗА ЗАБЛОКИРОВАНА\n\nAnti-Lust Guardian заблокировал угрозу на устройстве {device_id}.\nТип: {event_type}\nВремя: {timestamp}\n\nДействий не требуется.",
                    sms_text="🚨 Anti-Lust: Угроза заблокирована на {device_id}. Тип: {event_type}. Подробности в приложении.",
                    push_title="🛡️ Угроза Заблокирована",
                    push_body="Подозрительный контент перехвачен на {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Лимит Времени Исчерпан",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ ЛИМИТ ИСЧЕРПАН</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Оповещение об использовании,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Дневной лимит времени для <strong>{category}</strong> был достигнут на устройстве <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Статистика использования:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Категория:</strong> {category}</li>
                                        <li><strong>Лимит:</strong> {limit} минут</li>
                                        <li><strong>Статус:</strong> Заблокировано</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Управление лимитами</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="ЛИМИТ ИСЧЕРПАН\n\nУстройство {device_id} достигло лимита для {category}.\nДоступ ограничен.",
                    sms_text="⏳ Лимит: {device_id} достиг лимита {limit}м для {category}. Доступ заблокирован.",
                    push_title="⏳ Время Истекло",
                    push_body="{device_id} достиг лимита для {category}."
                )
            },
            'jp': {
                'threat_blocked': Template(
                    subject="🚨 脅威ブロック：不審なアクティビティを検出",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ 脅威を阻止しました</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>保護者様へ、</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Anti-Lust Guardianシステムは、監視対象デバイス上の潜在的な脅威を正常に遮断し、ブロックしました。
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">インシデント詳細：</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>タイプ：</strong> {event_type}</li>
                                        <li><strong>デバイス：</strong> {device_id}</li>
                                        <li><strong>時間：</strong> {timestamp}</li>
                                        <li><strong>信頼度：</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    アクションは不要です。コンテンツはユーザーに表示されませんでした。
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">完全なレポートを表示</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="脅威ブロック\n\nAnti-Lust Guardianはデバイス{device_id}上の脅威をブロックしました。\nタイプ：{event_type}\n時間：{timestamp}\n\nアクションは不要です。",
                    sms_text="🚨 Anti-Lust警告：{device_id}で脅威をブロックしました。タイプ：{event_type}。詳細はアプリで。",
                    push_title="🛡️ 脅威ブロック",
                    push_body="{device_id}で不審なコンテンツが遮断されました。"
                ),
                'time_limit': Template(
                    subject="⏳ 時間制限到達",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ 時間制限到達</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>使用アラート、</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    デバイス<strong>{device_id}</strong>で<strong>{category}</strong>の1日の時間制限に達しました。
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">使用統計：</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>カテゴリ：</strong> {category}</li>
                                        <li><strong>制限：</strong> {limit}分</li>
                                        <li><strong>ステータス：</strong> ロック中</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">制限を管理</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="時間制限到達\n\nデバイス{device_id}は{category}の制限に達しました。\nアクセスは制限されています。",
                    sms_text="⏳ 制限：{device_id}は{category}の{limit}分制限に達しました。アクセスロック。",
                    push_title="⏳ 時間切れ",
                    push_body="{device_id}は{category}の制限に達しました。"
                )
            },
            'cn': {
                'threat_blocked': Template(
                    subject="🚨 威胁已拦截：检测到可疑活动",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ 威胁已阻止</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>家长/监护人请注意，</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Anti-Lust Guardian 系统已成功拦截并阻止了受监控设备上的潜在威胁。
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">事件详情：</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>类型：</strong> {event_type}</li>
                                        <li><strong>设备：</strong> {device_id}</li>
                                        <li><strong>时间：</strong> {timestamp}</li>
                                        <li><strong>置信度：</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    无需采取行动。内容未显示给用户。
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">查看完整报告</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="威胁已拦截\n\nAnti-Lust Guardian 已阻止设备 {device_id} 上的威胁。\n类型：{event_type}\n时间：{timestamp}\n\n无需采取行动。",
                    sms_text="🚨 Anti-Lust 警报：设备 {device_id} 上的威胁已拦截。类型：{event_type}。查看应用详情。",
                    push_title="🛡️ 威胁已拦截",
                    push_body="在 {device_id} 上拦截了可疑内容。"
                ),
                'time_limit': Template(
                    subject="⏳ 达到时间限制",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ 限制已达</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>使用警报，</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    设备 <strong>{device_id}</strong> 已达到 <strong>{category}</strong> 的每日时间限制。
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">使用统计：</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>类别：</strong> {category}</li>
                                        <li><strong>限制：</strong> {limit} 分钟</li>
                                        <li><strong>状态：</strong> 已锁定</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">管理限制</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="达到时间限制\n\n设备 {device_id} 已达到 {category} 的限制。\n访问受限。",
                    sms_text="⏳ 限制：{device_id} 已达到 {category} 的 {limit} 分钟限制。访问已锁定。",
                    push_title="⏳ 时间到",
                    push_body="{device_id} 已达到 {category} 的限制。"
                )
            },
            'it': {
                'threat_blocked': Template(
                    subject="🚨 MINACCIA BLOCCATA: Rilevata Attività Sospetta",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ MINACCIA PREVENUTA</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Attenzione Genitore/Tutore,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Il sistema Anti-Lust Guardian ha intercettato e bloccato con successo una potenziale minaccia sul dispositivo monitorato.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Dettagli Incidente:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Tipo:</strong> {event_type}</li>
                                        <li><strong>Dispositivo:</strong> {device_id}</li>
                                        <li><strong>Ora:</strong> {timestamp}</li>
                                        <li><strong>Confidenza:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    Nessuna azione richiesta. Il contenuto non è stato mostrato all'utente.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Vedi Report Completo</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="MINACCIA BLOCCATA\n\nAnti-Lust Guardian ha bloccato una minaccia sul dispositivo {device_id}.\nTipo: {event_type}\nOra: {timestamp}\n\nNessuna azione richiesta.",
                    sms_text="🚨 Anti-Lust Alert: Minaccia bloccata su {device_id}. Tipo: {event_type}. Vedi app per dettagli.",
                    push_title="🛡️ Minaccia Bloccata",
                    push_body="Contenuto sospetto intercettato su {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Limite di Tempo Raggiunto",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ LIMITE RAGGIUNTO</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Avviso Utilizzo,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Il limite di tempo giornaliero per <strong>{category}</strong> è stato raggiunto sul dispositivo <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Statistiche Utilizzo:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Categoria:</strong> {category}</li>
                                        <li><strong>Limite:</strong> {limit} minuti</li>
                                        <li><strong>Stato:</strong> Bloccato</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Gestisci Limiti</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="LIMITE RAGGIUNTO\n\nIl dispositivo {device_id} ha raggiunto il limite per {category}.\nL'accesso è limitato.",
                    sms_text="⏳ Limite: {device_id} ha raggiunto il limite di {limit}m per {category}. Accesso bloccato.",
                    push_title="⏳ Tempo Scaduto",
                    push_body="{device_id} ha raggiunto il limite per {category}."
                )
            },
            'pt': {
                'threat_blocked': Template(
                    subject="🚨 AMEAÇA BLOQUEADA: Atividade Suspeita Detectada",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ AMEAÇA PREVENIDA</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Atenção Pai/Responsável,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    O sistema Anti-Lust Guardian interceptou e bloqueou com sucesso uma ameaça potencial no dispositivo monitorado.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">Detalhes do Incidente:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Tipo:</strong> {event_type}</li>
                                        <li><strong>Dispositivo:</strong> {device_id}</li>
                                        <li><strong>Hora:</strong> {timestamp}</li>
                                        <li><strong>Confiança:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    Nenhuma ação necessária. O conteúdo não foi exibido ao usuário.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Ver Relatório Completo</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="AMEAÇA BLOQUEADA\n\nAnti-Lust Guardian bloqueou uma ameaça no dispositivo {device_id}.\nTipo: {event_type}\nHora: {timestamp}\n\nNenhuma ação necessária.",
                    sms_text="🚨 Alerta Anti-Lust: Ameaça bloqueada em {device_id}. Tipo: {event_type}. Ver app para detalhes.",
                    push_title="🛡️ Ameaça Bloqueada",
                    push_body="Conteúdo suspeito interceptado em {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ Limite de Tempo Atingido",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ LIMITE ATINGIDO</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>Alerta de Uso,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    O limite de tempo diário para <strong>{category}</strong> foi atingido no dispositivo <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">Estatísticas de Uso:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>Categoria:</strong> {category}</li>
                                        <li><strong>Limite:</strong> {limit} minutos</li>
                                        <li><strong>Status:</strong> Bloqueado</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">Gerenciar Limites</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="LIMITE ATINGIDO\n\nO dispositivo {device_id} atingiu o limite para {category}.\nO acesso está restrito.",
                    sms_text="⏳ Limite: {device_id} atingiu o limite de {limit}m para {category}. Acesso bloqueado.",
                    push_title="⏳ Tempo Esgotado",
                    push_body="{device_id} atingiu o limite para {category}."
                )
            },
            'kr': {
                'threat_blocked': Template(
                    subject="🚨 위협 차단됨: 의심스러운 활동 감지됨",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ 위협 예방됨</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>부모님/보호자님께,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Anti-Lust Guardian 시스템이 모니터링 중인 기기에서 잠재적인 위협을 성공적으로 차단했습니다.
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">사건 세부 정보:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>유형:</strong> {event_type}</li>
                                        <li><strong>기기:</strong> {device_id}</li>
                                        <li><strong>시간:</strong> {timestamp}</li>
                                        <li><strong>신뢰도:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    조치가 필요하지 않습니다. 콘텐츠가 사용자에게 표시되지 않았습니다.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">전체 보고서 보기</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="위협 차단됨\n\nAnti-Lust Guardian이 기기 {device_id}에서 위협을 차단했습니다.\n유형: {event_type}\n시간: {timestamp}\n\n조치가 필요하지 않습니다.",
                    sms_text="🚨 Anti-Lust 알림: {device_id}에서 위협이 차단되었습니다. 유형: {event_type}. 앱에서 확인하세요.",
                    push_title="🛡️ 위협 차단됨",
                    push_body="{device_id}에서 의심스러운 콘텐츠가 차단되었습니다."
                ),
                'time_limit': Template(
                    subject="⏳ 시간 제한 도달",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ 제한 도달</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>사용 알림,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    기기 <strong>{device_id}</strong>에서 <strong>{category}</strong>의 일일 시간 제한에 도달했습니다.
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">사용 통계:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>카테고리:</strong> {category}</li>
                                        <li><strong>제한:</strong> {limit}분</li>
                                        <li><strong>상태:</strong> 잠김</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">제한 관리</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="시간 제한 도달\n\n기기 {device_id}가 {category} 제한에 도달했습니다.\n액세스가 제한됩니다.",
                    sms_text="⏳ 제한: {device_id}가 {category}의 {limit}분 제한에 도달했습니다. 액세스 잠김.",
                    push_title="⏳ 시간 종료",
                    push_body="{device_id}가 {category} 제한에 도달했습니다."
                )
            },
            'ar': {
                'threat_blocked': Template(
                    subject="🚨 تم حظر التهديد: تم اكتشاف نشاط مشبوه",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; direction: rtl;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ تم منع التهديد</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>عزيزي الوالد/ولي الأمر،</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    نجح نظام Anti-Lust Guardian في اعتراض وحظر تهديد محتمل على الجهاز المراقب.
                                </p>
                                <div style="background: #fff5f5; border-right: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">تفاصيل الحادث:</p>
                                    <ul style="color: #333333; margin: 10px 20px 0 0;">
                                        <li><strong>النوع:</strong> {event_type}</li>
                                        <li><strong>الجهاز:</strong> {device_id}</li>
                                        <li><strong>الوقت:</strong> {timestamp}</li>
                                        <li><strong>الثقة:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    لا يلزم اتخاذ أي إجراء. لم يتم عرض المحتوى للمستخدم.
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">عرض التقرير الكامل</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="تم حظر التهديد\n\nقام Anti-Lust Guardian بحظر تهديد على الجهاز {device_id}.\nالنوع: {event_type}\nالوقت: {timestamp}\n\nلا يلزم اتخاذ أي إجراء.",
                    sms_text="🚨 تنبيه Anti-Lust: تم حظر تهديد على {device_id}. النوع: {event_type}. راجع التطبيق للتفاصيل.",
                    push_title="🛡️ تم حظر التهديد",
                    push_body="تم اعتراض محتوى مشبوه على {device_id}."
                ),
                'time_limit': Template(
                    subject="⏳ تم الوصول إلى الحد الزمني",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; direction: rtl;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ تم الوصول للحد</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>تنبيه الاستخدام،</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    تم الوصول إلى الحد الزمني اليومي لـ <strong>{category}</strong> على الجهاز <strong>{device_id}</strong>.
                                </p>
                                <div style="background: #e6fffa; border-right: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">إحصائيات الاستخدام:</p>
                                    <ul style="color: #333333; margin: 10px 20px 0 0;">
                                        <li><strong>الفئة:</strong> {category}</li>
                                        <li><strong>الحد:</strong> {limit} دقيقة</li>
                                        <li><strong>الحالة:</strong> مقفل</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">إدارة الحدود</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="تم الوصول للحد الزمني\n\nوصل الجهاز {device_id} إلى الحد المسموح لـ {category}.\nتم تقييد الوصول.",
                    sms_text="⏳ الحد: وصل {device_id} إلى حد {limit} دقيقة لـ {category}. تم قفل الوصول.",
                    push_title="⏳ انتهى الوقت",
                    push_body="وصل {device_id} إلى الحد المسموح لـ {category}."
                )
            },
            'hi': {
                'threat_blocked': Template(
                    subject="🚨 खतरा अवरुद्ध: संदिग्ध गतिविधि का पता चला",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #ff2a6d; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛡️ खतरा रोका गया</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>ध्यान दें माता-पिता/अभिभावक,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    Anti-Lust Guardian सिस्टम ने निगरानी किए गए डिवाइस पर संभावित खतरे को सफलतापूर्वक रोक दिया है।
                                </p>
                                <div style="background: #fff5f5; border-left: 4px solid #ff2a6d; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #c53030; font-weight: bold;">घटना विवरण:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>प्रकार:</strong> {event_type}</li>
                                        <li><strong>डिवाइस:</strong> {device_id}</li>
                                        <li><strong>समय:</strong> {timestamp}</li>
                                        <li><strong>विश्वास:</strong> {confidence}%</li>
                                    </ul>
                                </div>
                                <p style="color: #666666; font-size: 14px;">
                                    किसी कार्रवाई की आवश्यकता नहीं है। सामग्री उपयोगकर्ता को नहीं दिखाई गई थी।
                                </p>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #ff2a6d; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">पूर्ण रिपोर्ट देखें</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="खतरा अवरुद्ध\n\nAnti-Lust Guardian ने डिवाइस {device_id} पर एक खतरे को रोक दिया है।\nप्रकार: {event_type}\nसमय: {timestamp}\n\nकिसी कार्रवाई की आवश्यकता नहीं है।",
                    sms_text="🚨 Anti-Lust चेतावनी: {device_id} पर खतरा अवरुद्ध। प्रकार: {event_type}। विवरण के लिए ऐप देखें।",
                    push_title="🛡️ खतरा अवरुद्ध",
                    push_body="{device_id} पर संदिग्ध सामग्री को रोका गया।"
                ),
                'time_limit': Template(
                    subject="⏳ समय सीमा समाप्त",
                    body_html="""
                    <html>
                    <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                            <div style="background: #05d5ff; padding: 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">⏳ सीमा समाप्त</h1>
                            </div>
                            <div style="padding: 30px;">
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong>उपयोग चेतावनी,</strong>
                                </p>
                                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                                    डिवाइस <strong>{device_id}</strong> पर <strong>{category}</strong> के लिए दैनिक समय सीमा समाप्त हो गई है।
                                </p>
                                <div style="background: #e6fffa; border-left: 4px solid #05d5ff; padding: 15px; margin: 20px 0;">
                                    <p style="margin: 0; color: #2c7a7b; font-weight: bold;">उपयोग आँकड़े:</p>
                                    <ul style="color: #333333; margin: 10px 0 0 20px;">
                                        <li><strong>श्रेणी:</strong> {category}</li>
                                        <li><strong>सीमा:</strong> {limit} मिनट</li>
                                        <li><strong>स्थिति:</strong> लॉक किया गया</li>
                                    </ul>
                                </div>
                                <div style="margin-top: 30px; text-align: center;">
                                    <a href="{dashboard_link}" style="background: #05d5ff; color: #ffffff; text-decoration: none; padding: 12px 25px; border-radius: 5px; font-weight: bold;">सीमाएँ प्रबंधित करें</a>
                                </div>
                            </div>
                        </div>
                    </body>
                    </html>
                    """,
                    body_text="समय सीमा समाप्त\n\nडिवाइस {device_id} ने {category} के लिए सीमा पार कर ली है।\nपहुँच प्रतिबंधित है।",
                    sms_text="⏳ सीमा: {device_id} ने {category} के लिए {limit} मिनट की सीमा पार कर ली है। पहुँच लॉक।",
                    push_title="⏳ समय समाप्त",
                    push_body="{device_id} ने {category} के लिए सीमा पार कर ली है।"
                )
            }
        }

    def get_template(self, language: str, template_name: str) -> Optional[Template]:
        lang_templates = self.templates.get(language, self.templates['en'])
        return lang_templates.get(template_name)
