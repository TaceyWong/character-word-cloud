import os
import wx
import wx.adv
import wx.lib.dialogs
from wx_helper import *



class ImageShowDialog ( wx.Dialog ):

	def __init__( self, parent,image):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.CAPTION|wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		bitmap = wx.Bitmap( image, wx.BITMAP_TYPE_ANY )
		bitmap = wx_scale_bitmap(bitmap,1080,986)
		self.Size = bitmap.Size
		
		self.m_bitmap9 = wx.StaticBitmap( self, wx.ID_ANY, bitmap, wx.DefaultPosition,bitmap.Size, 0 )
		bSizer5.Add( self.m_bitmap9, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer4 )
		self.Layout()
		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class MyFrame1
###########################################################################


class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 600,1000 ), style = wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
		self.mask_ori_path = "data/images/遮罩.png"
		self.mask_path = "data/images/遮罩.png"
		self.wc_path = "data/images/词云.png"
		self.wc = None
		self.mask = None
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.menubar = wx.MenuBar( 0 )
		self.program_menu = wx.Menu()
		self.refresh_menuItem = wx.MenuItem( self.program_menu, wx.ID_ANY, "刷新", wx.EmptyString, wx.ITEM_NORMAL )
		self.refresh_menuItem.SetBitmap( wx.Bitmap( "data/images/刷新.png", wx.BITMAP_TYPE_ANY ) )
		self.program_menu.Append( self.refresh_menuItem )

		self.exit_menuItem = wx.MenuItem( self.program_menu, wx.ID_ANY, "退出", wx.EmptyString, wx.ITEM_NORMAL )
		self.exit_menuItem.SetBitmap( wx.Bitmap( "data/images/exit.png", wx.BITMAP_TYPE_ANY ) )
		self.program_menu.Append( self.exit_menuItem )

		self.menubar.Append( self.program_menu, "程序" )

		self.help_menu = wx.Menu()
		self.doc_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, "使用文档", wx.EmptyString, wx.ITEM_NORMAL )
		self.doc_menuItem.SetBitmap( wx.Bitmap( "data/images/问号.png", wx.BITMAP_TYPE_ANY ) )
		self.help_menu.Append( self.doc_menuItem )

		self.update_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, "更新", wx.EmptyString, wx.ITEM_NORMAL )
		self.update_menuItem.SetBitmap( wx.Bitmap( "data/images/更新.png", wx.BITMAP_TYPE_ANY ) )
		self.help_menu.Append( self.update_menuItem )

		self.help_menu.AppendSeparator()

		self.about_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, "关于", wx.EmptyString, wx.ITEM_NORMAL )
		self.about_menuItem.SetBitmap( wx.Bitmap( "data/images/关于.png", wx.BITMAP_TYPE_ANY ) )
		self.help_menu.Append( self.about_menuItem )

		self.menubar.Append( self.help_menu, "帮助" )

		self.SetMenuBar( self.menubar )

		main_sizer = wx.BoxSizer( wx.HORIZONTAL )

		action_sizer = wx.BoxSizer( wx.VERTICAL )

		self.start_button = wx.Button( self, wx.ID_ANY, "生成词云", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.start_button.SetBitmap( wx.Bitmap( "data/images/启动.png", wx.BITMAP_TYPE_ANY ) )
		action_sizer.Add( self.start_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.start_staticline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		action_sizer.Add( self.start_staticline, 0, wx.EXPAND |wx.ALL, 5 )

		input_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, "输入设置" ), wx.VERTICAL )

		input_main_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		input_main_sizer.SetFlexibleDirection( wx.BOTH )
		input_main_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.select_mask_button = wx.Button( input_sizer.GetStaticBox(), wx.ID_ANY, "选择遮罩层图片", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.select_mask_button.SetBitmap( wx.Bitmap( "data/images/mask.png", wx.BITMAP_TYPE_ANY ) )
		input_main_sizer.Add( self.select_mask_button, 1, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.mask_path_text = wx.TextCtrl( input_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		input_main_sizer.Add( self.mask_path_text, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.select_stop_button = wx.Button( input_sizer.GetStaticBox(), wx.ID_ANY, "选择停用词文件", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.select_stop_button.SetBitmap( wx.Bitmap( "data/images/stop.png", wx.BITMAP_TYPE_ANY ) )
		input_main_sizer.Add( self.select_stop_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.stop_path_text = wx.TextCtrl( input_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		input_main_sizer.Add( self.stop_path_text, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.select_text_button = wx.Button( input_sizer.GetStaticBox(), wx.ID_ANY, "选择纯文本文件", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.select_text_button.SetBitmap( wx.Bitmap( "data/images/txt.png", wx.BITMAP_TYPE_ANY ) )
		input_main_sizer.Add( self.select_text_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.text_path_text = wx.TextCtrl( input_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		input_main_sizer.Add( self.text_path_text, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.select_freq_button = wx.Button( input_sizer.GetStaticBox(), wx.ID_ANY, "选择自频次文件", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.select_freq_button.SetBitmap( wx.Bitmap( "data/images/频次.png", wx.BITMAP_TYPE_ANY ) )
		input_main_sizer.Add( self.select_freq_button, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.freq_path_text = wx.TextCtrl( input_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		input_main_sizer.Add( self.freq_path_text, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )


		input_main_sizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		input_sizer.Add( input_main_sizer, 0, wx.EXPAND, 5 )

		fgSizer8 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText9 = wx.StaticText( input_sizer.GetStaticBox(), wx.ID_ANY, "选择mask提取模型", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		fgSizer8.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.model_choiceChoices = [ "u2net(缺省，通用解析模型)", "silueta(通用解析模型)", "u2net_human_seg(人形解析模型)", "u2net_cloth_seg(人体肖像布料解析模型)", 
						        "isnet-general-use(通用解析模型)", "isnet-anime(动漫角色解析模型)", "sam(通用解析模型)"]
		self.model_choice = wx.Choice( input_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.model_choiceChoices, 0 )
		self.model_choice.SetSelection( 0 )
		fgSizer8.Add( self.model_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.wword_cut_choice_label = wx.StaticText( input_sizer.GetStaticBox(), wx.ID_ANY, "选择中文分词模块", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.wword_cut_choice_label.Wrap( -1 )

		fgSizer8.Add( self.wword_cut_choice_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.word_cut_choiceChoices = [ "Jieba"]
		self.word_cut_choice = wx.Choice( input_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.word_cut_choiceChoices, 0 )
		self.word_cut_choice.SetSelection( 0 )
		fgSizer8.Add( self.word_cut_choice, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.colored_check = wx.CheckBox( input_sizer.GetStaticBox(), wx.ID_ANY, "依照蒙版色彩进行词云分布", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.colored_check.SetValue(True)
		self.colored_check.SetToolTip( "勾选后，词云将依照蒙版色彩进行分布。如果蒙版为黑白图片，即便勾选也不生效。" )
		fgSizer8.Add( self.colored_check, 0, wx.ALL, 5 )

		self.add_default_cleaner_check = wx.CheckBox( input_sizer.GetStaticBox(), wx.ID_ANY, "附加异常文本通用清洗", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.add_default_cleaner_check.SetValue(True)
		self.add_default_cleaner_check.SetToolTip("对文本中的HTML标签进行清洗")
		fgSizer8.Add( self.add_default_cleaner_check, 0, wx.ALL, 5 )

		self.add_default_stop_check = wx.CheckBox( input_sizer.GetStaticBox(), wx.ID_ANY, "附加基础停用词", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.add_default_stop_check.SetValue(True)
		self.add_default_stop_check.SetToolTip("附加缺省的中英文停用词")
		fgSizer8.Add( self.add_default_stop_check, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		input_sizer.Add( fgSizer8, 1, wx.EXPAND, 5 )


		action_sizer.Add( input_sizer, 1, wx.EXPAND, 5 )

		out_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, "输出设置" ), wx.VERTICAL )

		out_main_sizer = wx.FlexGridSizer( 0, 3, 0, 0 )
		out_main_sizer.SetFlexibleDirection( wx.BOTH )
		out_main_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.select_bg_color_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, "选择背景颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.select_bg_color_label.Wrap( -1 )

		out_main_sizer.Add( self.select_bg_color_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.bg_color_bitmap = wx.StaticBitmap( out_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( "data/images/background-color.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		out_main_sizer.Add( self.bg_color_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.bg_color_picker = wx.ColourPickerCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.WHITE, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		out_main_sizer.Add( self.bg_color_picker, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		# self.select_text_color_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, "选择文本颜色", wx.DefaultPosition, wx.DefaultSize, 0 )
		# self.select_text_color_label.Wrap( -1 )

		# out_main_sizer.Add( self.select_text_color_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		# self.text_color_bitmap = wx.StaticBitmap( out_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( "data/images/字体颜色.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		# out_main_sizer.Add( self.text_color_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		# self.text_color_picker = wx.ColourPickerCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.BLACK, wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
		# out_main_sizer.Add( self.text_color_picker, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.select_font_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, "选择文本字体", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.select_font_label.Wrap( -1 )

		out_main_sizer.Add( self.select_font_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.font_bitmap = wx.StaticBitmap( out_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( "data/images/字体.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		out_main_sizer.Add( self.font_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.font_choiceChoices = []
		self.font_choice = wx.Choice( out_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.font_choiceChoices, 0 )
		out_main_sizer.Add( self.font_choice, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.max_word_num_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, "最大词语数目", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.max_word_num_label.Wrap( -1 )

		out_main_sizer.Add( self.max_word_num_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )

		self.max_word_num_bitmap = wx.StaticBitmap( out_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( "data/images/数目.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		out_main_sizer.Add( self.max_word_num_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.max_word_num_spin = wx.SpinCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 10, 10000, 200 )
		out_main_sizer.Add( self.max_word_num_spin, 1, wx.ALL|wx.EXPAND, 5 )


		out_sizer.Add( out_main_sizer, 0, wx.EXPAND, 5 )

		fgSizer7 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.min_font_size_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, u"最小字体大小", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.min_font_size_label.Wrap( -1 )

		fgSizer7.Add( self.min_font_size_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.min_font_size_spin = wx.SpinCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 6 )
		fgSizer7.Add( self.min_font_size_spin, 0, wx.ALL|wx.EXPAND, 5 )

		self.max_font_size_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, u"最大字体大小", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.max_font_size_label.Wrap( -1 )

		fgSizer7.Add( self.max_font_size_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.max_font_size_spin = wx.SpinCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 45 )
		fgSizer7.Add( self.max_font_size_spin, 0, wx.ALL|wx.EXPAND, 5 )

		self.font_step_size_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, u"字体步长尺寸", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.font_step_size_label.Wrap( -1 )

		fgSizer7.Add( self.font_step_size_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.font_step_size_spin = wx.SpinCtrl( out_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 1 )
		fgSizer7.Add( self.font_step_size_spin, 0, wx.ALL|wx.EXPAND, 5 )

		self.mode_label = wx.StaticText( out_sizer.GetStaticBox(), wx.ID_ANY, u"生成图片模式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.mode_label.Wrap( -1 )

		fgSizer7.Add( self.mode_label, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		mode_choiceChoices = [ u"RGB背景非透明", u"RGBA背景透明" ]
		self.mode_choice = wx.Choice( out_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, mode_choiceChoices, 0 )
		self.mode_choice.SetSelection( 0 )
		fgSizer7.Add( self.mode_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )


		out_sizer.Add( fgSizer7, 1, wx.EXPAND, 5 )


		action_sizer.Add( out_sizer, 1, wx.EXPAND, 5 )


		main_sizer.Add( action_sizer, 1, wx.EXPAND, 5 )

		preview_sizer = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"预览区" ), wx.VERTICAL )

		ori_preview_sizer = wx.StaticBoxSizer( wx.StaticBox( preview_sizer.GetStaticBox(), wx.ID_ANY, u"原始遮罩图预览" ), wx.VERTICAL )

		self.open_ori_big_button = wx.Button( ori_preview_sizer.GetStaticBox(), wx.ID_ANY, u"查看大图", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.open_ori_big_button.SetBitmap( wx.Bitmap( "data/images/放大镜.png", wx.BITMAP_TYPE_ANY ) )
		self.open_ori_big_button.Disable()
		ori_preview_sizer.Add( self.open_ori_big_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticline1 = wx.StaticLine( ori_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		ori_preview_sizer.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		self.ori_preview_bitmap = wx.StaticBitmap( ori_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( "data/images/原始.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 200,200 ), 0 )
		ori_preview_sizer.Add( self.ori_preview_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		preview_sizer.Add( ori_preview_sizer, 1, wx.EXPAND, 5 )

		mask_preview_sizer = wx.StaticBoxSizer( wx.StaticBox( preview_sizer.GetStaticBox(), wx.ID_ANY, "遮罩图预览" ), wx.VERTICAL )

		fmask_preview_btn_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		fmask_preview_btn_sizer.SetFlexibleDirection( wx.BOTH )
		fmask_preview_btn_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.open_mask_big_button = wx.Button( mask_preview_sizer.GetStaticBox(), wx.ID_ANY, "查看大图", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.open_mask_big_button.SetBitmap( wx.Bitmap( "data/images/放大镜.png", wx.BITMAP_TYPE_ANY ) )
		self.open_mask_big_button.Disable()
		fmask_preview_btn_sizer.Add( self.open_mask_big_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.save_mask_button = wx.Button( mask_preview_sizer.GetStaticBox(), wx.ID_ANY, "保存大图", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.save_mask_button.SetBitmap( wx.Bitmap( "data/images/保存.png", wx.BITMAP_TYPE_ANY ) )
		self.save_mask_button.Disable()
		fmask_preview_btn_sizer.Add( self.save_mask_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		mask_preview_sizer.Add( fmask_preview_btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticline3 = wx.StaticLine( mask_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		mask_preview_sizer.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		self.mask_preview_bitmap = wx.StaticBitmap( mask_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap( self.mask_path, wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 200,200 ), 0 )
		mask_preview_sizer.Add( self.mask_preview_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		preview_sizer.Add( mask_preview_sizer, 1, wx.EXPAND, 5 )

		wc_preview_sizer = wx.StaticBoxSizer( wx.StaticBox( preview_sizer.GetStaticBox(), wx.ID_ANY, "词云图预览" ), wx.VERTICAL )

		wc_preview_btn_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
		wc_preview_btn_sizer.SetFlexibleDirection( wx.BOTH )
		wc_preview_btn_sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.open_wc_big_button = wx.Button( wc_preview_sizer.GetStaticBox(), wx.ID_ANY, "查看大图", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.open_wc_big_button.SetBitmap( wx.Bitmap( "data/images/放大镜.png", wx.BITMAP_TYPE_ANY ) )
		self.open_wc_big_button.Disable()
		wc_preview_btn_sizer.Add( self.open_wc_big_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.save_wc_button = wx.Button( wc_preview_sizer.GetStaticBox(), wx.ID_ANY, "保存大图", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.save_wc_button.SetBitmap( wx.Bitmap( "data/images/保存.png", wx.BITMAP_TYPE_ANY ) )
		self.save_wc_button.Disable()
		wc_preview_btn_sizer.Add( self.save_wc_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		wc_preview_sizer.Add( wc_preview_btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_staticline4 = wx.StaticLine( wc_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		wc_preview_sizer.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )

		self.wc_preview_bitmap = wx.StaticBitmap( wc_preview_sizer.GetStaticBox(), wx.ID_ANY, wx.Bitmap(self.wc_path, wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.Size( 200,200 ), 0 )
		wc_preview_sizer.Add( self.wc_preview_bitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		preview_sizer.Add( wc_preview_sizer, 1, wx.EXPAND, 5 )


		main_sizer.Add( preview_sizer, 1, wx.EXPAND, 5 )


		self.SetSizer( main_sizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.refresh_menuItemOnMenuSelection, id = self.refresh_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.exit_menuItemOnMenuSelection, id = self.exit_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.doc_menuItemOnMenuSelection, id = self.doc_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.update_menuItemOnMenuSelection, id = self.update_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.about_menuItemOnMenuSelection, id = self.about_menuItem.GetId() )
		self.start_button.Bind( wx.EVT_BUTTON, self.start_buttonOnButtonClick )
		self.select_mask_button.Bind( wx.EVT_BUTTON, self.select_mask_buttonOnButtonClick )
		self.select_stop_button.Bind( wx.EVT_BUTTON, self.select_stop_buttonOnButtonClick )
		self.select_text_button.Bind( wx.EVT_BUTTON, self.select_text_buttonOnButtonClick )
		self.select_freq_button.Bind( wx.EVT_BUTTON, self.select_freq_buttonOnButtonClick )
		self.model_choice.Bind( wx.EVT_CHOICE, self.model_choiceOnChoice )
		self.add_default_cleaner_check.Bind( wx.EVT_CHECKBOX, self.add_default_cleaner_checkOnCheckBox )
		self.add_default_stop_check.Bind( wx.EVT_CHECKBOX, self.add_default_stop_checkOnCheckBox )
		self.bg_color_picker.Bind( wx.EVT_COLOURPICKER_CHANGED, self.bg_color_pickerOnColourChanged )
		# self.text_color_picker.Bind( wx.EVT_COLOURPICKER_CHANGED, self.text_color_pickerOnColourChanged )
		# self.font_picker.Bind( wx.EVT_FONTPICKER_CHANGED, self.font_pickerOnFontChanged )
		self.mode_choice.Bind( wx.EVT_CHOICE, self.mode_choiceOnChoice )
		self.open_ori_big_button.Bind( wx.EVT_BUTTON, self.open_ori_big_buttonOnButtonClick )
		self.open_mask_big_button.Bind( wx.EVT_BUTTON, self.open_mask_big_buttonOnButtonClick )
		self.save_mask_button.Bind( wx.EVT_BUTTON, self.save_mask_buttonOnButtonClick )
		self.open_wc_big_button.Bind( wx.EVT_BUTTON, self.open_wc_big_buttonOnButtonClick )
		self.save_wc_button.Bind( wx.EVT_BUTTON, self.save_wc_buttonOnButtonClick )
		self.init_font_list()


	def __del__( self ):
		pass

	def init_font_list(self):
		from collections import OrderedDict
		from matplotlib import font_manager
		from fontTools.ttLib import TTFont
		self.font_map = OrderedDict()
		self.font_map["汉仪书简"] = "data/fonts/hysj.ttf"
		en_cn_map = {
			"KaiTi":"楷体","SimHei":"黑体","SimSun":"宋体","FangSong":"仿宋",
			"SimSun-ExtB":"新宋体","DengXian":"等线",
			"Microsoft YaHei":"微软雅黑"
		}
		for font_path in font_manager.findSystemFonts():
			try:
				font_name = TTFont(font_path)["name"].getName(1,3,1)
			except:
				font_name = font_manager.FontProperties(fname=font_path).get_name()
			font_name = str(font_name)
			self.font_map[en_cn_map.get(font_name,font_name)] = font_path
			
		for font_name,font_path in self.font_map.items():
			print(font_name,font_path)
			self.font_choice.Append(font_name)
		self.font_choice.SetSelection(0)
		
	# Virtual event handlers, override them in your derived class
	def refresh_menuItemOnMenuSelection( self, event ):
		event.Skip()
		self.UpdateWindowUI()

	def exit_menuItemOnMenuSelection( self, event ):
		event.Skip()
		exit()

	def doc_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def update_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def about_menuItemOnMenuSelection( self, event ):
		event.Skip()
		info = wx.adv.AboutDialogInfo()
		info.SetIcon(wx.Icon('data/images/icon.png', wx.BITMAP_TYPE_PNG))
		info.SetName('CharacterWordCloud')
		info.SetVersion('0.1.0')
		info.SetDescription('词云.')
		info.SetCopyright('© 2024 Tacey Wong')
		info.SetWebSite('https://cwc.icosmos.space')
		info.AddDeveloper('Tacey Wong')
		wx.adv.AboutBox(info)
		
	def check(self):
		# 检查是否输入文本
		if self.text_path_text.GetValue() == "":
			wx.MessageBox("请选择文本文件", "错误", wx.OK | wx.ICON_ERROR)
			return False
		# 检查停用词
		if self.stop_path_text.GetValue() == "" and not self.add_default_stop_check.GetValue():
			wx.MessageBox("在未使用缺省停用词的情况下没有选择停用词文件", "错误", wx.OK | wx.ICON_ERROR)
			return False
		return True
		

	def start_buttonOnButtonClick( self, event ):
		if not self.check():return
		from core import generate_mask,generate_stopwords,word_cut,generate_wordcloud

		dlg = wx.ProgressDialog("词云生成中","正在生成Mask...",maximum = 3,parent=self,
                               style = 0 | wx.PD_APP_MODAL |wx.PD_AUTO_HIDE)
		mask_ori_path = self.mask_path_text.GetValue()
		colored = self.colored_check.GetValue()
		model = self.model_choice.GetStringSelection().split("(")[0]
		kw = {}
		kw["max_font_size"] = self.max_font_size_spin.GetValue()
		kw["min_font_size"] = self.min_font_size_spin.GetValue()
		kw["max_words"] = self.max_word_num_spin.GetValue()
		kw["font_path"] =  self.font_map[self.font_choice.GetStringSelection()]
		kw["width"] = 400
		kw["height"] = 200
		kw["margin"] = 2
		kw["scale"] = 1 
		kw["stopwords"]=None
		kw["random_state"] = 42
		bg_color = list(self.bg_color_picker.GetColour())
		bg_color[-1]=155

		kw["background_color"] = "rgba{}".format(tuple(bg_color))
		kw["font_step"] = self.font_step_size_spin.GetValue()
		kw["mode"] = "RGBA" if "A" in self.mode_choice.GetStringSelection() else "RGB"
		kw["include_numbers"] = False
		kw["min_word_length"] = 0
		print(kw)
		if mask_ori_path:
			self.mask_path,self.mask = generate_mask(mask_ori_path,False,model)
			bitmap = wx.Bitmap(self.mask_path,wx.BITMAP_TYPE_ANY)
			self.mask_preview_bitmap.SetBitmap(wx_scale_bitmap(bitmap,200,200))
		wx.Yield()
		dlg.Update(1,"Mask生成完成;正在进行分词...")
		stopwords_paths = self.stop_path_text.GetValue().split("\x01")
		kw["stopwords"] = generate_stopwords(stopwords_paths) if stopwords_paths else set()
		text = word_cut(self.text_path_text.GetValue().split("\x01"))
		wx.Yield()
		dlg.Update(2,"中文分词完成;正在进行词云生成...")
		self.wc_path,self.wc = generate_wordcloud(text=text,
											mask_path=self.mask_path,
											colored=colored,**kw)
		bitmap = wx.Bitmap(self.wc_path,wx.BITMAP_TYPE_ANY)
		self.wc_preview_bitmap.SetBitmap(wx_scale_bitmap(bitmap,200,200))
		self.open_wc_big_button.Enable()
		self.save_wc_button.Enable()
		wx.Yield()
		dlg.Update(3,"词云生成完成")
		dlg.Destroy()

	def select_mask_buttonOnButtonClick( self, event ):
		wildcard = wildcard = "图片 (*.jpeg,*.jpg,*.png,*.bmp)|*.jpeg;*.jpg;*.png;*.bmp"
		dlg = wx.FileDialog(self, message="选取遮罩图片",
            defaultDir=os.path.join(os.path.dirname(__file__),"data/demo"),
            defaultFile="leijun.jpeg",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR  |  wx.FD_FILE_MUST_EXIST
        )
		if dlg.ShowModal() == wx.ID_OK:
			self.mask_path_text.SetValue(dlg.GetPath())
			if self.mask_path_text:
				bitmap = wx.Bitmap(self.mask_path_text.GetValue(),wx.BITMAP_TYPE_ANY)
				print(bitmap.Size)
				self.ori_preview_bitmap.SetBitmap(wx_scale_bitmap(bitmap,200,200))
				self.open_ori_big_button.Enable()
		dlg.Destroy()

	def select_stop_buttonOnButtonClick( self, event ):
		wildcard = "TXT纯文本 (*.txt)|*.txt"
		dlg = wx.FileDialog(self, message="选取停词表文档(支持按Ctrl多选)",
            defaultDir=os.path.join(os.path.dirname(__file__),"data/stop"),
            defaultFile="cn_stopwords.txt",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR  | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
        )
		if dlg.ShowModal() == wx.ID_OK:
			self.stop_path_text.SetValue("\x01".join(dlg.GetPaths()))
		dlg.Destroy()



	def select_text_buttonOnButtonClick( self, event ):
		wildcard = "TXT纯文本 (*.txt)|*.txt"
		dlg = wx.FileDialog(self, message="选取数据文本文件(支持按Ctrl多选)",
            defaultDir=os.path.join(os.path.dirname(__file__),"data/demo"),
            defaultFile="小米创业思考.txt",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR  | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
        )
		if dlg.ShowModal() == wx.ID_OK:
			self.text_path_text.SetValue("\x01".join(dlg.GetPaths()))
		dlg.Destroy()

	def select_freq_buttonOnButtonClick( self, event ):
		event.Skip()

	def model_choiceOnChoice( self, event ):
		event.Skip()

	def add_default_cleaner_checkOnCheckBox( self, event ):
		event.Skip()

	def add_default_stop_checkOnCheckBox( self, event ):
		event.Skip()

	def bg_color_pickerOnColourChanged( self, event ):
		print(event)
		print(self.bg_color_picker.GetColour())
		print(tuple(self.bg_color_picker.GetColour()))
		event.Skip()

	def text_color_pickerOnColourChanged( self, event ):
		event.Skip()

	def font_pickerOnFontChanged( self, event ):
		# from find_system_fonts_filename import get_system_fonts_filename
		# from matplotlib import font_manager
		# from fontTools.ttLib import TTFont
		# font = self.font_picker.GetSelectedFont()
		# print(font.GetNativeFontInfoDesc())
		# print(font.GetFaceName())
		# print(font.GetFamily())
		# print(font.GetWeight())
		# for f in font_manager.findSystemFonts():
		# 	fp = font_manager.FontProperties(fname=f)
		# 	print(fp.get_name())
		# 	try:
		# 		print(TTFont(f)["name"].getName(1,3,1))
		# 	except:
		# 		print("xxxx")
		# print("------")
		event.Skip()

	def mode_choiceOnChoice( self, event ):
		event.Skip()

	def open_ori_big_buttonOnButtonClick( self, event ):
		Image.open(self.mask_path_text.GetValue()).show()
		# dlg = ImageShowDialog(self,self.mask_path_text.GetValue())
		# dlg.ShowModal()
		# dlg.Destroy()
	def open_mask_big_buttonOnButtonClick( self, event ):
		Image.open(self.mask_path).show()
		# dlg = ImageShowDialog(self,self.mask_path)
		# dlg.ShowModal()
		# dlg.Destroy()

	def save_mask_buttonOnButtonClick( self, event ):
		dlg = wx.FileDialog(self, message=u"保存解析出的遮罩图", defaultFile="mask.png", 
					  wildcard=u"PNG图片 (*.png,*.jpg)|*.png;*.jpg", style=wx.FD_SAVE | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			self.mask.save(dlg.GetPath())
		dlg.Destroy()

	def open_wc_big_buttonOnButtonClick( self, event ):
		dlg = ImageShowDialog(self,self.wc_path)
		dlg.ShowModal()
		dlg.Destroy()

	def save_wc_buttonOnButtonClick( self, event ):
		dlg = wx.FileDialog(self, message=u"保存词云图", defaultFile="word-cloud.png", 
					  wildcard=u"PNG图片 (*.png,*.jpg)|*.png;*.jpg", style=wx.FD_SAVE | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			self.wc.to_file(dlg.GetPath())
		dlg.Destroy()





class CharacterWordCloudAPP(wx.App):
    def OnInit(self):
        # 界面语言设置为中文
        self.locale = wx.Locale(wx.LANGUAGE_CHINESE_CHINA)
        self.win = MainFrame(parent=None)
        self.SetTopWindow(self.win)
        self.win.SetTitle("Character Word Cloud v0.1.0 ❤ By Tacey Wong")
        self.win.SetIcon(wx.Icon("data/images/icon.png"))
        self.win.Show(True)
        return True

    def OnExit(self):
        exit()


if __name__ == '__main__':
    import sys,os,platform
    if platform.system() == 'Windows' and int(platform.version().split('.')[0]) >= 10:
        import ctypes; ctypes.windll.shcore.SetProcessDpiAwareness(1)
    CharacterWordCloudAPP(redirect=False).MainLoop()